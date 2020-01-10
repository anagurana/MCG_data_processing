import numpy as np
import scipy.signal

def powerSpectrum(x,Fs):
    freqs, ps = scipy.signal.periodogram(x, Fs, detrend='linear', scaling='spectrum', window='flattop')
    ps = np.sqrt(ps)
    freqs = freqs[1:] # Skip zero Hz element
    ps = ps[1:]
    return freqs, ps

def powerSpectralDensity(x, Fs):
    freqs, psd = scipy.signal.periodogram(x, Fs, detrend='linear', scaling='density', window='blackmanharris')
    psd = np.sqrt(psd)
    freqs = freqs[1:] # Skip zero Hz element
    psd = psd[1:]
    return freqs, psd

def averageNoise(freqs, psd, frange = (None, None)):
    fmin, fmax = frange
    if fmin:
        fmin_ind = freqs.searchsorted(fmin)
    else:
        fmin_ind = 0
    if fmax:
        fmax_ind = freqs.searchsorted(fmax)
    else:
        fmax_ind = freqs.size-1
    psdclip = psd[fmin_ind:fmax_ind]
    noiseAverage = np.sqrt( np.mean(psdclip**2) )
    return noiseAverage

def findFrequency(xin, fs, frange = (None, None), accurateAmplitude = True):
    fmin, fmax = frange

    # Returns amplitude, not RMS
    xin = np.array(xin)

    xin = xin-np.mean(xin)
    # Number of all samples
    N = xin.size

    # Apply the window
    win = scipy.signal.gaussian(N, N)
    x = xin*win

    # Perform the DFT
    X = np.fft.fft(x)

    # Get the phase and magnitude
    Xmag = np.abs(X)/np.sum(win)*2
    Xph  = np.angle(X)

    ind_fmin = 0
    ind_fmax = int(np.ceil(N/2))

    # Get the frequency vector
    freq = np.linspace(0, fs-1/fs, N)

    if fmin:
        ind_fmin = freq.searchsorted(fmin)

    if fmax:
        ind_fmax = freq.searchsorted(fmax)

    # Find the amplitude of the dominant frequency
    ind_max = ind_fmin+np.argmax(Xmag[ind_fmin:ind_fmax])

    # Extract the amplitude ...
    if accurateAmplitude:
        # Perform the DFT again without window
        X = np.fft.fft(xin)
        Xmag = np.abs(X)/(N/2)
    A = Xmag[ind_max]

    # ... frequency ..
    f0 = freq[ind_max]

    # ... phase (0..1)
    th = ( Xph[ind_max] + np.pi/2 )/( 2*np.pi )
    
    return A, f0, th

def logBin(freqs, psd, N=200, mode=1, verbosity=0):
    xs = freqs
    ys = psd
    # mode = 0 is for normal average
    # mode = 1 is for adding in quadrature
    # Data must be ascending in frequency
    if xs[0] == 0: # Avoid zero frequency
        xs = xs[1:]
        ys = ys[1:]
    df = xs[1] - xs[0]
    xmax = xs[-1]
    xmin = xs[0]
    maxlogx = np.log(xmax)
    minlogx = np.log(xmin)
    bins = np.exp(np.arange(N, dtype = float)/(N-1.)*(maxlogx-minlogx)+minlogx)
    bins[0] = xmin
    bins[-1] = xmax
    binindex = 1
    vi = 0
    sumy = 0
    sumx= 0
    count = 0
    binnedx = []
    binnedy = []
    try:
        while vi < len(xs) and binindex < len(bins):
            if verbosity>1:
                print('This bin is for X between %1.9e and %1.9e; current X = %1.9e'
                    %(bins[binindex-1], bins[binindex], xs[vi]))
            if bins[binindex-1] <= xs[vi] <= bins[binindex]:
                sumx = sumx + xs[vi]
                count = count + 1
                if mode == 0: sumy = sumy + ys[vi]
                if mode == 1: sumy = sumy + ys[vi]**2
                vi = vi + 1
            else:
                if xs[vi] > bins[binindex-1] and count == 0:
                    binindex = binindex + 1
                else:
                    #print(count)
                    binnedx.append(sumx/count)
                    if mode == 0: binnedy.append(sumy/count)
                    if mode == 1: binnedy.append(np.sqrt(sumy/count))
                    sumy = 0
                    sumx= 0
                    count = 0
                    binindex = binindex + 1
    except:
        print('logBin ERROR! Diagnostics:');
        print('vi',vi)
        print('binindex',binindex)
        print('len(bins)',len(bins))
        print("len(xs)",len(xs))
        print('bins[binindex-1]',bins[binindex-1])
        print("xs[vi]",xs[vi])
        raise Exception("logBin Failed")
    return np.array(binnedx),np.array(binnedy)

