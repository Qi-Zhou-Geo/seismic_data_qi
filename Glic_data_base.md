## User manual of seismic_data_qi
This is the user manual for members of the **“Hazards and Surface Processes Research Group and the Digital Earth Lab”** to access seismic data on the GFZ Glic server.

**Author: Qi Zhou** <br>
**Maintenance: Qi Zhou**

## 1, Preparation
### 1.1, Glic Account
Please make sure you have the GLIC account, <br>
if not, please contact the GFZ IT to apply one.

### 1.2, Python Environment for Obspy
Please refer this link to deploy your own python environmet, <br>
[Click here to see how to install conda on Glic](https://git-int.gfz-potsdam.de/hpc/user-manual/-/wikis/env#conda), <br>

for example, <br>
I create a envs named as **seismic**, <br>
and install **Obspy** package.
```sh
conda create --name seismic
conda activate seismic
conda install conda-forge::obspy
```

Finally, please double check that your python environment **seismic** has successfully installed Obspy! <br>

### 1.3, R Environment for Eseis (Not recommended)
If you want to use [Eseis](https://www.gfz-potsdam.de/en/section/geomorphology/projects/eseis) to process seismic data,
you can create a R environmet named as **r-base**, <br>
```bash
conda activate
conda create --name r-env r-essentials r-base
conda activate --stack r-env
R --version
conda deactivate
```
Please be super careful when you install **Eseis**,
#### 1.3.1, prepare the package for r-env
Please note: #eseis# package is not available via conda <br>
open terminal and active the envs **r-env**, <br>
```sh
conda install -c conda-forge r-essentials # install the essentials package
```
then install **terra**, **fftw**, and other package.
```sh
conda install -c r r-terra # https://docs.anaconda.com/free/working-with-conda/reference/r-language-pkg-docs/
```

#### 1.3.2, install #eseis# package
Please make sure all the eseis required packaged, then install #eseis# package , <br>
type **R** in terminal to entre the R, <br>

```sh
install.packages("eseis", repos="https://cloud.r-project.org")
```
then type
```sh
q()
```

### 1.4, sbatch file for Python
Prepare a **example.sh** file with the following information, <br>
and make sure you have the test.py
```sh
#!/bin/bash
#SBATCH -t 4-00:00:00              # time limit: (D-HH:MM:SS) 
#SBATCH --job-name=Qi_run          # job name, "Qi_run"
#SBATCH --ntasks=1                 # each individual task in the job array will have a single task associated with it
#SBATCH --mem-per-cpu=8G		       # Memory Request (per CPU; can use on GLIC)

source /your/path/for/miniforge3/bin/activate
conda activate seismic

run python /your/python/file/path/test.py
```

### 1.5, sbatch file for R (Not recommended)
Prepare a **example.sh** file with the following information, <br>
and make sure you have the test.R

```sh
#!/bin/bash
#SBATCH -t 4-00:00:00              # time limit: (D-HH:MM:SS) 
#SBATCH --job-name=Qi_run          # job name, "Qi_run"
#SBATCH --ntasks=1                 # each individual task in the job array will have a single task associated with it
#SBATCH --mem-per-cpu=8G		       # Memory Request (per CPU; can use on GLIC)

CONDA_BASE=$(conda info --base) 
source "${CONDA_BASE}/etc/profile.d/conda.sh"
conda activate 
conda activate --stack r-env

Rscript /your/python/file/path/test.R
```

## 2, Shared Group Folder
Path **/storage/vast-gfz-hpc-01/project/seismic_data_qi** <br>
please do NOT overwrite or delete any file.

## 3, Access Seismic Data
You can use this code to fetch and convert the seismic data to numpy,
```python
#!/usr/bin/python
# -*- coding: UTF-8 -*-

#__modification time__ = 2024-04-28
#__author__ = Qi Zhou, Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences
#__find me__ = qi.zhou@gfz-potsdam.de, qi.zhou.geo@gmail.com, https://github.com/Nedasd
# Please do NOT distribute this code without the author's permission

from obspy import read, Stream, UTCDateTime, read_inventory

global SAC_PATH, OUTPUT_DIR
SAC_PATH = "/storage/vast-gfz-hpc-01/project/seismic_data_qi/seismic/EU/Illgraben/"
OUTPUT_DIR = "/storage/vast-gfz-hpc-01/home/qizhou/1projects/" # set your output path

print(SAC_PATH)

def load_seismic_signal(data_start, data_end, station, component="EHZ", remove_sensor_response=False):
    '''
    Load seismic signal

    Parameters:
    - data_start (str): the start time to select data, e.g., 2017-04-03 12:00:00
    - data_end (str): the start time to select data, e.g., 2017-04-03 13:00:00
    - station (str): seismic station name
    - component (str): seismic component name
    - remove_sensor_response (bool, optial): for deconvolove

    Returns:
    - st (obspy.core.stream): seismic stream
    '''

    d1 = UTCDateTime(data_start)
    d2 = UTCDateTime(data_end)

    sac_dir = f"{SAC_PATH}{d1.year}/{station}/{component}/"

    if d1.year in [2013, 2014]:
        seismic_network = "GM"
    elif d1.year in [2017, 2018, 2019, 2020]:
        seismic_network = "9S"


    if d1.julday == d2.julday:
        data_name = f"{seismic_network}.{station}.{component}.{d1.year}.{str(d1.julday).zfill(3)}"
        st = read(sac_dir + data_name)
    else:
        st = Stream()
        for n in np.arange(d1.julday, d2.julday+1):
            data_name = f"{seismic_network}.{station}.{component}.{d1.year}.{str(n).zfill(3)}"
            st += read(sac_dir + data_name)


    st = st.trim(starttime=d1, endtime=d2, nearest_sample=False)
    st.merge(method=1, fill_value='latest', interpolation_samples=0)
    st._cleanup()
    st.detrend('linear')
    st.detrend('demean')
    st.filter("bandpass", freqmin=1, freqmax=45)


    if remove_sensor_response is True:
        inv = read_inventory(f"{SAC_PATH}metadata_2017-2020.xml")
        st.remove_response(inventory=inv)

    return st

data_start, data_end, station = "2017-06-09 12:00:00", "2017-06-09 18:00:00", "ILL12"
st = load_seismic_signal(data_start, data_end, station, component="EHZ", remove_sensor_response=False)
st.plot(outfile=f"{OUTPUT_DIR}{data_start}")
```
