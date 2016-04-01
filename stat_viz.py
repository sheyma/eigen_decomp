import numpy as np
import h5py
sys.path.append(os.path.expanduser('/home/raid/bayrak/devel/brainsurfacescripts'))


def get_surface(surface_data, hemisphere, surface_type):
    """
    surface_data = hdf5 formatted surface data
    hemisphere = 'LH', 'RH', or 'full'
    surface_type = 'midthickness', 'inflated', or 'very_inflated'
    """
    tmp = h5py.File(surface_data, 'r')
    indices = np.array( tmp[hemisphere][surface_type]['indices'] )
    vertices = np.array( tmp[hemisphere][surface_type]['vertices'] )    
    triangles = np.array( tmp[hemisphere][surface_type]['triangles'])
    
    return indices, vertices, triangles


surface_data = '/nobackup/kocher1/bayrak/tmp/' + 'data_surface.h5'
surface_type = 'midthickness'

n_lh, vertices_lh, triangles_lh = get_surface(surface_data, 'LH', surface_type)

n_rh, vertices_rh, triangles_rh = get_surface(surface_data, 'RH', surface_type)

path = '/nobackup/kocher1/bayrak/palm_results_SCPTs_NEW/'

import glob

cont = glob.glob(path + '/LH_01_dpv_ztstat_cfdrp_c3.csv') # LH_01*p_c1.csv')
anti = glob.glob(path + '/LH_01_dpv_ztstat_cfdrp_c4.csv') #LH_01*p_c2.csv')

CONT = glob.glob(path + '/RH_01_dpv_ztstat_cfdrp_c3.csv') # LH_01*p_c1.csv')
ANTI = glob.glob(path + '/RH_01_dpv_ztstat_cfdrp_c4.csv') #LH_01*p_c2.csv')


list_cont = []; list_CONT = [];
list_anti = []; list_ANTI = [];

for i in range(0, len(cont)):
    for j in range(0, len(anti)):
        if cont[i][:-5] == anti[j][:-5]:        
            for k in range(0, len(CONT)):
                if CONT[k][49:-5] == cont[i][49:-5]:
                    for l in range(0, len(ANTI)):
                        if cont[i][49:-5] == ANTI[l][49:-5]:
            
                            print cont[i]
                            print anti[j]
                            print CONT[k]
                            print ANTI[l]    

                            list_cont.append(cont[i])
                            list_anti.append(anti[j])
                            list_CONT.append(CONT[k])
                            list_ANTI.append(ANTI[l])
            
threshold = True
o = 2
for i in range(0, len(list_cont)):
    if list_cont[i][:-5] != list_anti[i][:-5]:
        print "FUCK"
    #print list_cont[i]
    #print list_anti[i]
    x = np.ones(len(vertices_lh))
    y = np.ones(len(vertices_rh))
    
    F = np.loadtxt(list_cont[i], delimiter = ',')    
    E = np.loadtxt(list_anti[i], delimiter = ',')

    K = np.loadtxt(list_CONT[i], delimiter = ',')
    L = np.loadtxt(list_ANTI[i], delimiter = ',')

    if threshold:
        
        f_index = np.where(F[n_lh] < 0.05)
        x[n_lh[f_index]] = F[n_lh[f_index]]
    
        e_index = np.where(E[n_lh] < 0.05)
        x[n_lh[e_index]] = -1 * E[n_lh[e_index]]
    
        x[np.where(x==1)] = 0.06
        #print x.max(), x.min()
        
        k_index = np.where(K[n_rh] < 0.05)
        y[n_rh[k_index]] = K[n_rh[k_index]]        
        
        l_index = np.where(L[n_rh] < 0.05)
        y[n_rh[l_index]] = -1 * L[n_rh[l_index]]

        y[np.where(y==1)] = 0.06

        if np.shape(e_index)[1] != 0 and np.shape(f_index)[1] != 0 and np.shape(k_index)[1] != 0 and np.shape(l_index)[1] != 0:
            print x.max(), x.min()

            plot_surf_stat_map(vertices_lh, triangles_lh, o, '221', stat_map=x,
                               cmap='jet', azim=180, threshold=0.05, 
                               figsize=(10,10))
            plot_surf_stat_map(vertices_lh, triangles_lh, o, '223', stat_map=x,
                               cmap='jet', azim=0, threshold=0.05, 
                               figsize=(10,10))
                               
            plot_surf_stat_map(vertices_rh, triangles_rh, o, '222', stat_map=y,
                               cmap='jet', azim=0, threshold=0.05, 
                               figsize=(10,10))

            plot_surf_stat_map(vertices_lh, triangles_lh, o, '224', stat_map=y,
                               cmap='jet', azim=180, threshold=0.05, 
                               figsize=(10,10))
                               
                               
        o += 1
     
     
     
       
       

#F = np.loadtxt(path + 'LH_01_dpv_ztstat_cfdrp_c3.csv', delimiter=',')
#f_index = np.where(F[n_lh] < 0.05)
#x[n_lh[f_index]] = F[n_lh[f_index]]
#
#E = np.loadtxt(path + 'LH_01_dpv_ztstat_cfdrp_c4.csv', delimiter=',')
#e_index = np.where(E[n_lh] < 0.05)
#x[n_lh[e_index]] = -1 * E[n_lh[e_index]]
#
#x[np.where(x==1)] = 0.06
#
#plot_surf_stat_map(vertices_lh, triangles_lh, 1, '221', stat_map=x, 
#                   cmap='jet', azim=180,  threshold = 0.05, figsize=(10,10))
#                   
##
#if set(e_index[0]).intersection(f_index[0]) != 0:
#    print "OVERLAP" 







