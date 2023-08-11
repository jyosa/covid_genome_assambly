import os
import subprocess
import config
import sys
import argparse
from emailme import emailme
from datetime import datetime
import fnmatch
import config
import subprocess
import pandas as pd
import shutil

def depth(namerun):
    name = namerun
    
    initname = name + '_barcode'
    aver = []
    barcode = []
    for filename in os.listdir("./"):
        if filename.startswith(initname) and  filename.endswith("sorted.bam"):
            namelist = filename.split('.')
            if namelist[1] == 'sorted':
                #barcode.append(filename.split('.')[0])
                subsam = config.samtools + ' depth ' + filename + ' > data.dat'
                subprocess.call(subsam, shell=True,stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
                empty = os.stat('data.dat').st_size==0
                if empty == True:
                    pass
                else:
                    barcode.append(filename.split('.')[0])
                    df = pd.read_csv('data.dat', sep='\t')
                    df.columns = ['reads','num','num2']
                    aver.append(df['num2'].mean())
    dicti = dict(zip(barcode, aver))
    data_items = dicti.items()
    data_list = list(data_items)
    dfdict = pd.DataFrame(data_list)
    dfdict.to_csv('depth.csv')
    print('File depth.csv was generate!!!')


def articProtocol(run_name,fast5,mini,maxi,accuracy,num_callers,gpu_runners_per_device,chunks_per_runner,numGpus,email='No'):
    start_time = datetime.now()

    def basecaller(fast5,run_name,accuracy,num_callers=8,gpu_runners_per_device=64,chunks_per_runner=256,numGpus=1):
        if accuracy == 'high':
            accuracy = config.guppy_cfg_hac
        elif accuracy == 'fast':
            accuracy = config.guppy_cfg_fast
        else:
            print("\nno es un argumento valido para el modo Basecalling, por favor elija entre high o fast\n\n")
            exit()
        if numGpus == 1:
            baserun = config.basecaller + ' --disable_pings --compress_fastq -c ' + accuracy + \
' --num_callers ' + str(num_callers) + ' --gpu_runners_per_device ' + str(gpu_runners_per_device) +\
'  --chunks_per_runner ' + str(chunks_per_runner) + ' -i ' + \
fast5 + ' -s ' + run_name + ' --device ' + 'cuda:0  -r'
            subprocess.call(baserun, shell=True)
        else:
            gpus=[]
            for g in range(numGpus):
                gpus.append('cuda:' + str(g))
            gpusUsed = '"' + ' '.join(gpus) + '"'
            baserun = config.basecaller + ' --disable_pings --compress_fastq -c '+ accuracy + \
' --num_callers ' + str(num_callers) + ' --gpu_runners_per_device ' + str(gpu_runners_per_device) +\
' --chunks_per_runner ' + str(chunks_per_runner) +  ' -i ' + \
fast5 + ' -s ' + run_name + ' --device ' + gpusUsed + ' -r'
            subprocess.call(baserun, shell=True)
        

    maxamplicon = maxi + 200
    if os.path.isdir(run_name):
        print("\nCuidado!!!!!!!!!\nEl directorio de nombre {} existe \
este puede tener resultados previos, cambie el nombre y vuelva\
a correr el script.\n\n".format(run_name))
        exit()
    else:
        os.mkdir(run_name)

    os.chdir(run_name)


    ambiente = os.environ["CONDA_PREFIX"].split('/')
    if ambiente[-1] == 'artic':
        #Correr basecaller
        basecaller(fast5,run_name,'high',numGpus=numGpus)

        #Correr barcode
        barcodSub = config.barcoder + " --require_barcodes_both_ends -i " + run_name + " -s output --config configuration.cfg --barcode_kits EXP-NBD196"
        subprocess.call(barcodSub, shell=True)

        for filename in os.listdir('output/'):
            path='output/' + filename
            if filename.startswith('barcode') and os.path.isdir(path):
                subfilt = 'artic guppyplex --min-length ' + str(mini) + ' --max-length ' + str(maxamplicon) +\
' --directory output/' + filename + ' --prefix ' + run_name
                subprocess.call(subfilt, shell=True)

        #Correr minion pipeline
        Barcodes = run_name + '_barcode'
        listBarcodes = []
        for barnames in os.listdir('./'):
            if barnames.startswith(Barcodes): 
                listBarcodes.append(barnames)
                namebar = list(barnames.split("."))
                samplename = namebar[0]
                sec_summ = run_name + '/sequencing_summary.txt'
                subArticMin = 'artic minion --normalise 200 --threads 4 --scheme-directory ~//home/juvenal/fieldbioinformatics/primer_schemes --read-file ' +\
barnames + ' --fast5-directory ' + fast5 + ' --sequencing-summary ' + sec_summ + ' SARS-CoV-2/V4.1 ' + samplename
                print("Juvisssss. {}".format(subArticMin))
                subprocess.call(subArticMin, shell=True)
        if len(listBarcodes) == 0:
            print("\nNo hay resultados para artic guppyplex, revise sus datos o pregunte a su bioinform'atico de confinaza!!!!\n\n")
            emailfailtxt = "\nNo hay resultados para artic guppyplex, revise sus datos o pregunte a su bioinform'atico de confinaza!!!!\n\n"
            exit()
        consen = 'cat *.consensus.fasta > my_consensus_genomes.fasta'
        subprocess.call(consen, shell=True)
        os.chdir('..')
#        compress = 'tar -cvzf ' + run_name + '.tgz ' + run_name + '/'
#        subprocess.call(compress, shell=True)
#        deleteFold = 'rm -rf ' + run_name
#        subprocess.call(deleteFold, shell=True)
        pwd =  os.getcwd()
#        res = pwd + '/' + run_name + '.tgz'
        depth(run_name)
        


        end_time = datetime.now()
        print('\n\n##########################################################\nduraci\'o del protocolo artic para {}: {}\n\n\
Los resultados los encuentra en: \n{}\n\
##########################################################\n\n'.format(run_name,end_time - start_time,run_name))
        date_time = datetime.now()
        contmail = "\nHola el Protocolo artic-ncov2019 ha finalizado para "  + run_name + " en " + str(date_time) + "\n\n archivo adjunto: my_consensus_genomes.fasta.\n Que tengas un excelente d'ia!!!!\n\nPowered by @El_Dryosa"
        contmail2 = "\nHola el Protocolo artic-ncov2019 ha finalizado para "  + run_name + " en " + str(date_time) + "\n\n archivo adjunto: depth.csv.\n Que tengas un excelente d'ia!!!!\n\nPowered by @El_Dryosa"

        
        if email == 'Si':
            emailme(contmail,'my_consensus_genomes.fasta')
            emailme(contmail2,'depth.csv')
        elif email == 'si':
            emailme(contmail,'my_consensus_genomes.fasta')
            emailme(contmail2,'depth.csv')
        elif email == 'No':
            print("No se enviar notificaci'on")
        elif email == 'no':
            print("No se neviar'a notificaci'on")
        else:
            print("{} no es una opci'on valida no se envira'a un emailde notificaci'on".format(email))

    else:
        print("Antes de correr el protocolo artic debe activar el ambiente artic-ncov2019:\n\n$ conda activate artic-ncov2019\n\n")

if __name__ == "__main__":


    # Argumentos
    ap = argparse.ArgumentParser()
    ap.add_argument("-r", "--run_name", type=str, required=True,
        help="Nombre del proyecto")
    ap.add_argument("-f", "--fast5", type=str, required=True,
        help="Path completo donde se encuentra el directorio con los archivos fast5 ej. '/home/jyosa/fast5'")
    ap.add_argument("-m", "--min", type=int, required=True,
        help="longitud m'inima de los amplicones")
    ap.add_argument("-x", "--max", type=int, required=True,
        help="longitud m'axima de los amplicones")
    ap.add_argument("-a", "--accuracy", type=str, required=True,
        help="Ejecute la basecaller de Guppy con el modo de precisi'on alta o r'apida, valores = 'fast' y 'high'")
    ap.add_argument("-g", "--num_callers", type=int, default=8, required=False,
        help="Numero de basecallers paralelos a crear, valor por default = 8")
    ap.add_argument("-k", "--gpu_runners_per_device", type=int, default=64, required=False,
        help="Etiqueta para maximizar la utilizaci'on de la GPU, valor por default = 64")
    ap.add_argument("-i", "--chunks_per_runner", type=int, default=256, required=False,
        help="Chunks m'aximos por corrida,valor por default = 256")
    ap.add_argument("-j", "--numGpus", type=int, default=1, required=False,
        help="N'umero de GPUs a utilizar, valor por default = 1")
    ap.add_argument("-e", "--email", type=str, default="No", required=False,
        help="Si quiere que le avise por email que ha terminado todo el protocolo -e = Si, valor por default = No")
    args = vars(ap.parse_args())    


    run_name = args["run_name"]
    fast5 = args["fast5"]
    mini = args["min"]
    maxi = args["max"]
    accuracy = args["accuracy"]
    num_callers = args["num_callers"]
    gpu_runners_per_device = args["gpu_runners_per_device"]
    chunks_per_runner = args["chunks_per_runner"]
    numGpus = args["numGpus"]
    email = args["email"]

    articProtocol(run_name,fast5,mini,maxi,accuracy,num_callers,gpu_runners_per_device,chunks_per_runner,numGpus,email)






