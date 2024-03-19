
import logging
import math
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import savgol_filter
from scipy.interpolate import interp1d

'''
measuring the asymmetry of river a la Finotello et al. 2024 -
Vegetation Enhances Curvature-Driven Dynamics in Meandering
Rivers, 2024, Nature Communication
'''

def make_logger(logname="mylog",level=logging.WARNING, log_to_file=False):

    personal_note_logger = logging.getLogger(logname)
    personal_note_logger.setLevel(level)

    # Define a formatter for log messages
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(funcName)s() [line %(lineno)d] - %(message)s')

    # Create a stream handler to output log messages to the console
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    personal_note_logger.addHandler(stream_handler)

    # Optionally, create a file handler to save log messages to a file
    if log_to_file:
        file_handler = logging.FileHandler('personal_note.log')
        file_handler.setFormatter(formatter)
        personal_note_logger.addHandler(file_handler)

    return personal_note_logger

def xy_coord(centerline_coordinates: np.ndarray) -> np.ndarray:
    '''
    return path as x,y pairs
    '''

    x_coordinates = []
    y_coordinates = []

    # splitting centerline coordinaets into an x and y component
    for centerline_point in centerline_coordinates:
        x_coordinates.append(centerline_point[0])
        y_coordinates.append(centerline_point[1])

    return np.array(x_coordinates),np.array(y_coordinates)

def find_curvature(x: np.ndarray,y:np.ndarray)-> np.ndarray:
    '''
    find curvature at each point on path
    '''

    dx = np.gradient(x)
    dy = np.gradient(y)
    ddx = np.gradient(dx)
    ddy = np.gradient(dy)
    curvature_path = np.abs(dx * ddy - dy * ddx) / (dx ** 2 + dy ** 2) ** 1.5

    return curvature_path

def smooth_curvature(curvature_path: np.ndarray, poly_order: int = 3, window_size: int = 21) -> np.ndarray:
    '''
    smooth curvature using low-pass filter (Savitzky–Golay)
    '''

    smoothed_curvature = savgol_filter(curvature_path, window_size, poly_order)

    return smoothed_curvature

def find_inflection_pt_index(x_points: np.ndarray,y_points: np.ndarray) -> np.ndarray:
    '''
    find where the slope of the curvature
    changes sign from negative to positive
    ie half of the inflection points
    '''

    # interpolate to get continuous function
    lin_interp = interp1d(x_points, y_points, kind='linear')

    x_interp = np.linspace(x_points[0], x_points[-1], len(x_points))
    y_interp = lin_interp(x_interp)
    dy_interp = np.gradient(y_interp, x_interp)

    # Find where the derivative changes sign
    inflection_pt_indx = np.where(np.diff(np.sign(dy_interp)) > 0)[0]

    return inflection_pt_indx


def find_apex_index(smoothed_curvature: np.ndarray, inflection_pt_index: np.ndarray) -> np.ndarray:
    '''
    find river apex indices aka points of max curvature
    between successive inflection points
    '''

    apex_index = []
    for i in range(len(inflection_pt_index) - 1):
        start_index = inflection_pt_index[i]
        end_index = inflection_pt_index[i + 1]
        if start_index != end_index:
            max_index = start_index + np.argmax(smoothed_curvature[start_index:end_index])
            apex_index.append(max_index)

    return np.array(apex_index)

def streamwise_distances(x,y,start_index,end_index):
    def distance(x1, y1, x2, y2):
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    total_dist = 0
    for i in range(start_index,end_index):
        total_dist += distance(x[i], y[i], x[i+1], y[i+1])

    return total_dist

def wavelength_asymmetry(x,y, apex_index, inflection_pt_index):
    '''
    see  Finotello+2024 fig. 2

    (lu) upstream component =
    distance from first inflection point to apex (traveling downstream)
    (ld) downstream component =
    distance from apex to next inflection point (traveling downstream)

    instrinic wavelength = lu + ld

    '''

    lu = []
    ld = []
    instric_wavelength = []
    asymmetry = []

    mylog.warning("Something weird is happening here. "
                    "Not sure why the distances keep getting bigger. "
                    "Fix this.")

    for i in range(len(inflection_pt_index) - 1):
        start_index = inflection_pt_index[i]
        mid_index = apex_index[i]
        end_index = inflection_pt_index[i+1]
        lu.append(streamwise_distances(x,y,start_index,mid_index))
        ld.append(streamwise_distances(x,y,mid_index,end_index))
        instric_wavelength.append(lu[i] + ld[i])
        asymmetry.append((lu[i] - ld[i])/instric_wavelength[i])

    return instric_wavelength, asymmetry


def main() -> None:

    mylog.info('Running module RiverAsymmetry as main. Example using artifical river shape\n')

    # RANDOM RIVER SHAPE
    num_pts = 1000
    scl = 0.01
    t = np.linspace(0, 10*np.pi, num_pts)
    x = t
    y = np.sin(t) #+ np.random.normal(scale=scl, size=num_pts)


    # CALCULATE STUFF
    curv = find_curvature(x,y)
    scurv = smooth_curvature(curv)

    ip_idx = find_inflection_pt_index(t,scurv)
    apex =  find_apex_index(scurv,ip_idx)

    wv_len, asym = wavelength_asymmetry(x,y, apex, ip_idx)


    # PLOT STUFF

    fig, axs = plt.subplots(2)
    axs[0].plot(x,y,'k.-')

    #axs[1].plot(t,curv,'k.-', label = 'curvature')
    axs[1].plot(t,scurv,'k.-', label = 'smoothed curvature')

    for ind in ip_idx:
        axs[1].axvline(x=t[ind], color='r', linestyle='--', alpha=0.5)

    plt.scatter(t[apex], scurv[apex], color='r', label='Apex')

    axs[0].set_title('River Shape')
    axs[0].set_xlabel('x')
    axs[0].set_ylabel('y')
    axs[1].set_title('Curvature')
    axs[1].set_xlabel('downstream')
    axs[1].set_ylabel('curvature')
    plt.legend()
    plt.show()


    fig, axs = plt.subplots(2)
    axs[0].scatter(ip_idx[:-1],wv_len,color='b')
    axs[1].scatter(ip_idx[:-1],asym,color='r')
    plt.show()


if __name__ == '__main__':

    mylog = make_logger(level=logging.INFO)
    main()

