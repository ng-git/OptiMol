import pandas as pd
import numpy as np
import xgboost as xgb
import math
import pkg_resources

from scipy import stats
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.multioutput import MultiOutputRegressor

from optimol import data_compile

ROOT = pkg_resources.resource_filename('optimol', '')

def get_csv():
    '''return demo datafrme'''
    return pd.read_csv(ROOT + '/model.csv')

def get_centroid(coord_matrix):
    '''calculate centroid of 2d or 3d matrix'''
    centroid = np.mean(coord_matrix)
    return centroid

def translation_centroid(coord_matrix):
    '''move 2d or 3d matrix centroid to origin'''
    translated_matrix = coord_matrix - get_centroid(coord_matrix)
    return translated_matrix

def get_max_dist(coord_matrix):
    '''get the index of the atom that have largest distance to centroid'''
    dist = (coord_matrix)**2
    dist = np.sum(dist, axis=1)
    dist = np.sqrt(dist)
    dist_index = dist.idxmax()
    return dist_index

def unit_vector(vector):
    '''Returns the unit vector of the vector. '''  
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    '''Returns the angle in radians between vectors 'v1' and 'v2':: '''
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    angle = np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))
    if(v1_u[0]*v2_u[1] - v1_u[1]*v2_u[0] < 0):
        angle = -angle
    return angle

def rotation_matrix_2d(theta):
    '''for 2d matrix, get the rotational matrix given the traget angle theta'''
    r = np.array(((np.cos(theta), -np.sin(theta)),
               (np.sin(theta),  np.cos(theta))))
    return r

def absmax_index(a, axis=None):
    '''find the second atom index that is used
    to align y axis for 3d matrix
    due to the addition of DOF'''
    amax = a.max(axis)
    max_index = a.idxmax()
    amin = a.min(axis)
    min_index = a.idxmin()
    if -amin > amax:
        result = min_index
    else:
        result = max_index
    return result

def translate_rotate_2d(coord_2d):
    '''Translate and rotate the 2d matrix
    so that the centroid is located at origin
    and the furtherest atom is located at x axis
    Param 
    coord_2d: input 2d structure of the atom
    Return 
    max_x_index: the index of the furtherest atom
    coord_2d_new: competed 2d matrix that has the
    translation and rotation
    '''
    trans_matrix = translation_centroid(coord_2d)
    max_x_index = get_max_dist(trans_matrix)
    base = [1,0]
    theta = angle_between(base,trans_matrix.iloc[max_x_index])
    r_matrix = rotation_matrix_2d(theta)
    coord_2d_new = trans_matrix.dot(r_matrix).round(4)
    # get the y axis index to be aligned for the 3d matrix
    y_index = absmax_index(coord_2d_new[1])
    return max_x_index, y_index, coord_2d_new

def rotation_matrix_from_vectors(vec1, vec2):
    """ Find the rotation matrix that aligns vec1 to vec2
    :param vec1: A 3d "source" vector
    :param vec2: A 3d "destination" vector
    :return mat: A transform matrix (3x3) which when applied to vec1, aligns it with vec2.
    """
    a, b = (vec1 / np.linalg.norm(vec1)).reshape(3), (vec2 / np.linalg.norm(vec2)).reshape(3)
    v = np.cross(a, b)
    c = np.dot(a, b)
    s = np.linalg.norm(v)
    kmat = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    rotation_matrix = np.eye(3) + kmat + kmat.dot(kmat) * ((1 - c) / (s ** 2))
    return rotation_matrix

def rotation_around_x(axis, theta):
    """
    Return the rotation matrix associated with counterclockwise rotation about
    the given axis by theta radians.
    """
    axis = np.asarray(axis)
    axis = axis / math.sqrt(np.dot(axis, axis))
    a = math.cos(theta / 2.0)
    b, c, d = -axis * math.sin(theta / 2.0)
    aa, bb, cc, dd = a * a, b * b, c * c, d * d
    bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
    return np.array([[aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
                     [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
                     [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc]])

def translate_rotate_3d(x_index, y_index, coord_3d):
    '''Translate and rotate the 2d matrix
    so that the centroid is located at origin
    and the furtherest atom is located at x axis
    Param 
    coord_2d: input 2d structure of the atom
    Return 
    max_x_index: the index of the furtherest atom
    coord_2d_new: competed 2d matrix that has the
    translation and rotation
    '''
    # center 3d
    centered_y = translation_centroid(coord_3d)
    base_x = [1,0,0]
    # rotate 3d
    rotate_matrix_x = rotation_matrix_from_vectors(np.array(centered_y.iloc[x_index]),base_x)
    x_rotated = rotate_matrix_x.dot(centered_y.T).T.round(4)
    # align y axis
    # get y axis to be aligned
    y_align = x_rotated[y_index]
    # get norm of y vector
    eucli = np.linalg.norm(y_align)
    # get targeted position of y coordinates
    y_coord = np.sqrt(eucli**2-y_align[0]**2)
    new_coord = [y_align[0],y_coord,0]
    # get rotational angle to be rotated around x axis
    angle_test = angle_between(y_align[1:3],new_coord[1:3])
    # finally rotate y axis
    completed_y = np.dot(rotation_around_x([1,0,0], angle_test), x_rotated.T).T.round(4)
    return completed_y

def build_model():
    id_list = data_compile.get_id()
    full = pd.DataFrame()
    for i in id_list:
        data_2d = data_compile.get_df_database(i)[0]
        head_2d = data_2d[['2d_x','2d_y']]
        tail_2d = data_2d[['periodic_#_2d','bond_1_2d','bond_2_2d','bond_3_2d']]
        x_index, y_index, head_2d_new = translate_rotate_2d(head_2d)
        full_2d = pd.concat([head_2d_new, tail_2d], axis=1, sort=False)
        data_3d = data_compile.get_df_database(i)[2]
        full_3d = data_3d[['3d_x','3d_y','3d_z']]
        full_3d = pd.DataFrame(translate_rotate_3d(x_index, y_index, full_3d))
        full_mole = pd.concat([full_2d,full_3d], axis=1, sort=False)
        full = full.append(full_mole)
    full.columns = ['2d_x','2d_y','periodic_#_2d','bond_1_2d','bond_2_2d','bond_3_2d','3d_x','3d_y','3d_z']
    full.to_csv(r'model.csv')
    
def get_model(data):
    data_drop_na = data.astype(float).dropna()
    X_full = data_drop_na[['2d_x','2d_y','periodic_#_2d','bond_1_2d','bond_2_2d','bond_3_2d']].reset_index(drop=True)
    Y_full = data_drop_na[['3d_x','3d_y','3d_z']].reset_index(drop=True)
    param = {
    'booster': 'gbtree',
    'learning_rate': 0.1,
    'subsample': 1,
    'gamma': 0,
    'n_estimators': 100,
    'colsample_bytree': 0.5,
    'max_depth': 10,
    'objective': 'reg:squarederror',
    'seed': 2} 
    multioutputregressor = MultiOutputRegressor(xgb.XGBRegressor(**param)).fit(X_full, Y_full)
    return multioutputregressor

def model_eval(model,data,n_fold=5):
    data_drop_na = data.astype(float).dropna()
    X_full = data_drop_na[['2d_x','2d_y','periodic_#_2d','bond_1_2d','bond_2_2d','bond_3_2d']].reset_index(drop=True)
    Y_full = data_drop_na[['3d_x','3d_y','3d_z']].reset_index(drop=True)
    score = model.score(X_full, Y_full)
    kfold = KFold(n_splits=n_fold, random_state=5)
    results = cross_val_score(model, X_full, Y_full, cv=kfold)
    print("Accuracy: %.2f%% (%.2f%%)" % (score*100, results.std()*100))
    
def predict_3d(user_input,model):
    user_output = model.predict(user_input)
    user_output = pd.DataFrame(user_output, columns = ['3d_x','3d_y','3d_z'])
    return user_output
