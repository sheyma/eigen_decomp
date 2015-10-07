"""Load NIfTI-1 (neuroinformatics technology initiative) file format 
"""

def load_nii(subject, template, cnt_files, dtype=None):
                
    """Load NIfTI-1 formatted data structures and return them as numpy array
     
     subject : string
        Subject is a directory with all scanned data of an individual. We are 
        using freely available data from Human Connectome Project (HCP), which
        releases almost 500 subjects with their subject-id numbers. 
        (e.g. subject = 'data_path/100307/')
        /a/documents/connectome/_all/100307  
    template : string 
        Template is the sketch-name of *.nii files (NIfTI-1 format) of interest
        for a subject. Each subject directory has many *.nii files, but we are 
        pointing the ones of our interest with the template string. 
        (e.g., resting-state data of a subject is sketched as below, 
        template = 'rfMRI_REST?_??_Atlas_hp2000_clean.dtseries.nii'  
        teplate =  'MNINonLinear/Results/rfMRI_REST?_??/rfMRI_REST?_??_Atlas_hp2000_clean.dtseries.nii
        this will be converted into these forms after loop:
        
        rfMRI_REST1_LR_Atlas_hp2000_clean.dtseries.nii
        rfMRI_REST1_RL_Atlas_hp2000_clean.dtseries.nii
        rfMRI_REST2_LR_Atlas_hp2000_clean.dtseries.nii
        rfMRI_REST2_RL_Atlas_hp2000_clean.dtseries.nii )
    
    cnt_files : int
        Number of *.nii files of interest for a subject. 
        (e.g. for resting-state data, cnt_files = 4)
        
    K : output, numpy.ndarray
        Concetanated matrices obtained from each *.nii file. 
        
    # python version 2.7.3
    # numpy version 1.9.1 """
             
    from glob import glob
    import os
    import numpy as np
    import nibabel as nb
        
    files = [val for val in sorted(glob(os.path.join(subject, template)))]
    files = files[:cnt_files]

    for x in xrange(0, cnt_files):
        print "AAAAAAAAAAAAAAA"        
        print x, files[x]
        img = nb.load(files[x])
        
        # brainModels[2] will include both left and right hemispheres
        # for only left hemisphere: brainModels[1]

        # count of brain nodes 
        n = img.header.matrix.mims[1].brainModels[2].indexOffset

        single_t_series = img.data[:, :n].T

        # length of time series 
        m = single_t_series.shape[1]

        m_last = m
        n_last = n

        mean_series = single_t_series.mean(axis=0)
        std_series = single_t_series.std(axis=0)

        if x == 0:
            # In first loop we initialize matrix K to be filled up and returned
            # By default we are using the same dtype like input file (float32)
            init_dtype = single_t_series.dtype if dtype == None else dtype
            K = np.ndarray(shape=[n,m], dtype=init_dtype, order='F')
        else:
            if  m_last != m:
                print "Warning, %s contains time series of different length" % (subject)
            if  n_last != n:
                print "Warning, %s contains different count of brain nodes" % (subject)
            K.resize([n, K.shape[1] + m])

        # concatenation of normalized time-series, column-wise
        K[:, -m:] = (single_t_series - mean_series) / std_series
        del img
        del single_t_series
    # transpose of K, columns are brain nodes, rows are time-series
    return K.T