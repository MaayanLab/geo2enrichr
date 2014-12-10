import matplotlib.pyplot as plt
import os
import numpy as np
from collections import defaultdict as ddict
import QuantileNormalization
from collections import Counter
import math
from decimal import Decimal
from scipy.stats import fisher_exact
from scipy.stats.stats import pearsonr
import re
import scipy

os.chdir("C:\\Users\\Rotation\\Desktop\\AxelStuff")


#Gets datafile as list of lines
def getWordList(file):
    '''Returns contents of file as a list of lowercase strings'''
    datafile = open(file,"r")
    wordlist = [word.lower().strip() for word in datafile]
    datafile.close()
    return wordlist
    
def normalizeData(data_list, rebuild = True):
    patient_id = data_list[2].split('\t') #Initiate parts of data table
    gene_id = []
    data_matrix = []
    
    for line in data_list[3:]: #Separate data matrix
        split_line = line.split('\t')
        gene_id.append(split_line[0])
        data_values = [float(x) for x in split_line[2:]]
        data_matrix.append(data_values)
    array_matrix = np.array(data_matrix) #Turn list into array for normalization
    norm_matrix = np.ma.masked_array(array_matrix, mask = np.zeros((len(array_matrix[0]),len(array_matrix))))
    ##norm_matrix = QuantileNormalization.quantile_normalization(array_matrix) #Normalize data matrix
    QuantileNormalization.quantile_norm(norm_matrix)
    norm_matrix = np.array(norm_matrix)
    
    if rebuild:
        rebuildMatrix(norm_matrix,gene_id,patient_id)
    else:
        return norm_matrix, gene_id, patient_id[2:]


def rebuildMatrix(norm_matrix,gene_id,patient_id):
    norm_matrix = norm_matrix.tolist() #Reconstruct matrix to include headers and labels
    for index in range(len(norm_matrix)):
        norm_matrix[index-1].insert(0,gene_id[index-1]) #add in gene information
    norm_matrix.insert(0,patient_id)#add in patient information
    norm_matrix[0].insert(0,0)
    return norm_matrix
    
def significantExpr(data_matrix,stdevs): #takes input of a matrix with one line for patient header and one column for gene ids
    patient_updict = ddict(list)
    patient_downdict = ddict(list)
    print data_matrix[0]
    patient_names = data_matrix[0]
    
    for line in data_matrix[1:]: #ignore patient names for the moment
        data_values = line[1:] #ignore gene names for the moment
        mean = np.mean(data_values)
        std = np.std(data_values)
        for value in data_values:
            patient = patient_names[data_values.index(value) + 1]
            if (value - stdevs*std) > mean:
                patient_updict[patient].append(line[0])
            elif (value + stdevs*std) < mean:
                patient_downdict[patient].append(line[0])
                
    return (patient_updict, patient_downdict)
                
    
def writeGMT(dictionary,output): #Writes any given dictionary to a GMT format
    write_file = open(output,'w')
    for e in dictionary:
        if isinstance(e, str):
            write_file.write(e + '\t' + '\t'.join(dictionary[e]) + '\n')
        
##To generate expression GMTs: getWordList(datafile) -> sigValues(datalist, zscore) -> writeGMT

def exprDataGMT(datafile,zscore): #wrapper type thing
    print("Retrieving Data")
    wordList = getWordList(datafile)
    print ("Normalizing Data")
    normData = normalizeData(wordList)
    print ("Determining Significant Expression")
    sigExpr = significantExpr(normData, zscore)
    print ("Writing GMT files")
    writeGMT(sigExpr[0],datafile[:-4] + '_up.GMT')
    writeGMT(sigExpr[1],datafile[:-4] + '_down.GMT')
    
    
    
def findHighVariability((norm_matrix, gene_id, patient_id)):
    varriance_dict = {}
    patient_list = patient_id[2:] #remove annoying headers
    norm_matrix = np.array(norm_matrix)
    for gene_index in range(len(norm_matrix)):
        varriance_dict[np.var(norm_matrix[gene_index-1])] = (gene_id[gene_index-1],norm_matrix[gene_index-1])
    
    varriances = varriance_dict.keys() #create dictionary of variances
    varriances.sort()
    h_var_list = varriances[-1000:]
    
    h_var_matrix = []
    h_var_genes = []
    
    for var in h_var_list:
        h_var_matrix.append(varriance_dict[var][1]) #add files to list of data and genes for high varianc
        h_var_genes.append(varriance_dict[var][0])
    return np.array(h_var_matrix),h_var_genes, patient_id
    

def readClusters(cluster_file): #read a file of numbered designated clusters
    cluster_dict = ddict(list)
    cluster_lines = getWordList(cluster_file)
    current_cluster = ''
    for line in cluster_lines:
        if not line[0].isalpha():
            current_cluster = line[0]
        else:
            cluster_dict[current_cluster].append(line)
    return cluster_dict

def readOutcomes(outcome_file): #reads an outcome file
    outcome_dict = {}
    outcome_lines = getWordList(outcome_file)
    for outcome in outcome_lines[1:]:
        split_outcome = outcome.split('\t')
        outcome_dict[split_outcome[0]] = split_outcome[1:] #remove header because it is uninteresting
    return outcome_dict

def sortClusterOutcomes(cluster_file,outcome_file): #combine outcome and cluster information
    death_dict = ddict(list)
    rec_dict = ddict(list)
    cluster_dict = readClusters(cluster_file)
    outcome_dict = readOutcomes(outcome_file)
    for cluster in cluster_dict:
        for patient in cluster_dict[cluster]:
            if patient in outcome_dict and outcome_dict[patient][0] == '1': #did the patient die from liver cancer
                death_dict[cluster].append((patient, outcome_dict[patient][1]))
            if patient in outcome_dict and outcome_dict[patient][2] == '1':
                rec_dict[cluster].append((patient,outcome_dict[patient][3])) #did the patient have a reccuring event
    return death_dict,rec_dict
    
def plotKaplanMeier(event_dict,threshold,title): #calculate a kaplan meier plot based on a dictionary of events given a threshold of cluster size
    cluster_event_dict = {}
    fig, ax = plt.subplots()
    cluster_list = []
    for cluster in event_dict:
        if len(event_dict[cluster]) > threshold:
            cluster_list.append(cluster)
            event_list = event_dict[cluster]
            times = [int(event[1]) for event in event_list]
            sorted_times = sorted(times)
            sorted_times.insert(0,0)
            initial_patients = float(len(event_list))
            survivor_list = [(initial_patients - sorted_times.index(e)) for e in sorted_times]
            survivor_list = [survivors/initial_patients for survivors in survivor_list]
            cluster_event_dict[cluster] = (survivor_list,sorted_times)
            ax.step(sorted_times,survivor_list,label = cluster,drawstyle='steps-post',linewidth=6)
            plt.xlabel('Time',size = 30)
            plt.ylabel('Percentage of Uncensored Patients Alive', size = 30)
            plt.title(title,size = 48)
    legend = ax.legend(loc='upper right', shadow=True, prop={'size':36})
    plt.show()
    return cluster_event_dict
    ##return sorted_times, survivor_list
    

def logRankVariance(Oj,N1j,Nj): #calculate variance for log rank function
    numerator = Oj*(N1j/Nj)*(1-N1j/Nj)*(Nj-Oj)
    denomenator = Nj - 1
    return numerator/denomenator

def logRank((N1,O1),(N2,O2)): #calculate log rank z-score
    numerator_sum = []
    denomenator_sum = []
    j_list = O1[1:] + O2[1:]
    print len(j_list)
    j_list = sorted(j_list)
    for j in j_list:
        O1J = float(O1.count(j))
        OJ = float(O1.count(j) + O2.count(j))
        N1J = float(len([time for time in O1 if time > j]))
        N2J = float(len([time for time in O2 if time > j]))
        NJ = float(len([time for time in j_list if time > j])) #Variable inputs to equation for log-rank
        
        if NJ > 1:    
            E1J = (OJ/NJ)*N1J  
            numerator_sum.append(O1J-E1J)
            denomenator_sum.append(logRankVariance(OJ,N1J,NJ))
    return sum(numerator_sum)/math.sqrt(sum(denomenator_sum))
        
def readGMT(gmt_file): #reads a GMT file into a dictionary
    GMT_dict = {}
    gmt_lines = getWordList(gmt_file)
    for line in gmt_lines:
        split_line = line.split('\t')
        GMT_dict[split_line[0]] = split_line[1:]
    return GMT_dict
    
def computeFisherExact(gene_list1, gene_list2): #computes the fisher exact test 
    set_list1 = set(gene_list1)
    set_list2 = set(gene_list2)
    n = 20000 #arbitrary number estimating total genes but not triny too hard to estimate accurately
    a = len(set_list1.intersection(set_list2))
    b = len(set_list1) - a
    c = len(set_list2) - a
    d = n - a - b - c
    return fisher_exact([[a,b],[c,d]])
    
def fisherExactTwoGMT(gmt_file1, gmt_file2): #runs down two separate GMT file and performs the fisher exact test, outputting a data matrix
    
    gmt_dict1 = readGMT(gmt_file1)
    gmt_dict2 = readGMT(gmt_file2)
    gmt_keys1 = gmt_dict1.keys()
    gmt_keys2 = gmt_dict2.keys()
   
    data_matrix = np.zeros((len(gmt_keys1),len(gmt_keys2)))
    
    for entry1 in gmt_keys1:
        print ('row ' + str(gmt_keys1.index(entry1) + 1) + ' out of ' + str(len(gmt_keys1)))
      
        for entry2 in gmt_keys2:
            data_matrix[gmt_keys1.index(entry1)][gmt_keys2.index(entry2)] = computeFisherExact(gmt_dict1[entry1],gmt_dict2[entry2])[1]
    
    return data_matrix,gmt_keys2,gmt_keys1
    
    
    
def printDataMatrix(data_matrix,output_file): #prints a data matrix composed of the matrix itself, column labels, and row labels
    output_write = open(output_file,'w')
    for line in data_matrix:
        line = [str(e) for e in line]
        output_write.write('\t'.join(line) + '\n')
    output_write.close()
        
    
def readDataMatrix(data_file):
    matrix_lines = getWordList(data_file)
    col_labels = matrix_lines[0].split('\t')[1:]
    data_matrix = []
    row_labels = []
    for line in matrix_lines[1:]:
        split_line = line.split('\t')
        row_labels.append(split_line[0])
        values = [float(x) for x in split_line[1:]]
        data_matrix.append(values)
    return np.array(data_matrix),row_labels,col_labels
    
    
    

def getPatientExpr(data_file):
    matrix_read = readDataMatrix(data_file)
    data_matrix = matrix_read[0].tolist()
    gene_list = matrix_read[1]
    patient_list = matrix_read[2]
    p_expr_dict = {}
    for p in patient_list:
        p_expr_dict[p] = {}
    
    print len(data_matrix)
    for row_index in range(len(data_matrix)):
        row = data_matrix[row_index]

        for col_index in range(len(row)):
            expr_value = row[col_index]
            patient = patient_list[col_index]
            gene = gene_list[row_index]
            p_expr_dict[patient][gene] = expr_value
    return p_expr_dict
            
            
    
    
def createCoorMatrix(less_genes,more_genes): #predicts genes from more_genes dictionary to a patient in less_genes dictionary
    
    less_gene_dict = getPatientExpr(less_genes)
    more_gene_dict = getPatientExpr(more_genes)
    less_gene_keys = less_gene_dict.keys()
    more_gene_keys = more_gene_dict.keys()
    corr_matrix = np.zeros((len(less_gene_keys),len(more_gene_keys)))
    common_genes = list(set(less_gene_dict[less_gene_keys[0]]).intersection(set(more_gene_dict[more_gene_keys[0]])))
    print len(common_genes)
    for less_patient in less_gene_keys:
        row_index = less_gene_keys.index(less_patient)
        for more_patient in more_gene_keys:
            col_index = more_gene_keys.index(more_patient)
            less_gene_values = [less_gene_dict[less_patient][gene] for gene in common_genes]
            more_gene_values = [more_gene_dict[more_patient][gene] for gene in common_genes]
            corr = pearsonr(np.array(less_gene_values),np.array(more_gene_values))[0]
            corr_matrix[row_index][col_index] = corr
    
    print "Predicting Genes"
    
    for corr_row in corr_matrix.tolist():
        less_patient = less_gene_keys[corr_matrix.tolist().index(corr_row)]
        print less_patient
        highest_corr = more_gene_keys[corr_row.index(max(corr_row))]
        for gene_key in more_gene_dict[highest_corr]:
            if gene_key not in common_genes:
                less_gene_dict[less_patient][gene_key] = more_gene_dict[highest_corr][gene_key]        
            
    return corr_matrix, less_gene_keys, more_gene_keys, less_gene_dict, more_gene_dict

def matrixFromDict(p_gene_dict):
    patients = p_gene_dict.keys()
    genes = p_gene_dict[patients[0]].keys()
    data_matrix = np.zeros((len(genes),len(patients)))
    print data_matrix
    for g in genes:
        print genes.index(g)
        for p in patients:
            data_matrix[genes.index(g)][patients.index(p)] = p_gene_dict[p][g]
    return data_matrix,genes,patients
            

def makeTCGAintoMatrix(directory):
    
    file_gene_dict = {}
    os.chdir(directory)
    file_list = os.listdir(os.getcwd())
    for file_name in file_list:
        if "normalized_results" in file_name and "genes" in file_name:
            data_file = getWordList(file_name)
            file_gene_dict[file_name] = {}
            for line in data_file[1:]:
                split_line = line.split('\t')
                gene_match = re.match('(\w+)|',split_line[0])
                gene = gene_match.group()
                file_gene_dict[file_name][gene] = split_line[1]
    return file_gene_dict

def convertRNASeqToPatients(seq_list,convert_file):
    convert_list = getWordList(convert_file)
    convert_dict = {}
    barcode_list = []
    for convert_line in convert_list[1:]:
        split_line = convert_line.split('\t')
        data_file = split_line[21]
        tcga_barcode = split_line[1]
        convert_dict[data_file] = tcga_barcode
    print len(convert_dict)
    print len(set(seq_list).intersection(set(convert_dict.keys())))
    for file_name in seq_list:
        converted_file = convert_dict[file_name]
        barcode_list.append(converted_file)
    return barcode_list
    
def readTCGAOutcomes(data_file):
    tcga_outcome_dict = {}
    line_list = getWordList(data_file)
    for line in line_list:
        split_line = line.split('\t')
        tcga_id = split_line[0]
        vital_status = split_line[9]
        days_to_death = split_line[11]
        if vital_status == 'dead':
            try:
                num_days = float(days_to_death)
                tcga_outcome_dict[tcga_id] = num_days
            except ValueError:
                print 'Days to death not found'
    return tcga_outcome_dict
    
def sortTCGAOutcomes(cluster_file,outcome_file): #combine outcome and cluster information
    death_dict = ddict(list)
    cluster_dict = readClusters(cluster_file)
    outcome_dict = readTCGAOutcomes(outcome_file)
    for cluster in cluster_dict:
        for patient in cluster_dict[cluster]:
            if patient in outcome_dict:
                death_dict[cluster].append((patient, outcome_dict[patient]))
    return death_dict

def dataFileToDataMatrix(data_file):
    matrix_list = []
    data_list = getWordList(data_file)
    split_list = [line.split('\t') for line in data_list]
    matrix_list.append(split_list[0])
    for value_line in split_list[1:]:
        gene = [value_line[0]]
        values = [float(x) for x in value_line[1:]]
        gene.extend(values)
        matrix_list.append(gene)
    return matrix_list
    
def createClusterMatrix(gmt_file, cluster_p_list):
    patient_list = getWordList(cluster_p_list)
    gmt_dict = readGMT(gmt_file)
    abrv_dict = {}
    patient_dict = {}
    for p in gmt_dict:
        print p[:12]
        abrv_dict[p[:12]] = gmt_dict[p]
    for patient in patient_list:
        if patient in abrv_dict:
            patient_dict[patient] = abrv_dict[patient]
    return patient_dict
    
def clusterColors(color_list, top_color):
    new_c = ''
    old_c = ''
    leaf_c = []
    for color in color_list:
        new_c = color
        if old_c == new_c:
            leaf_c.append(new_c)
        else:
            leaf_c.append(old_c)
            leaf_c.append(new_c)
        old_c = color
    leaf_c.remove('')
    #while top_color in leaf_c:
     #   leaf_c.remove(top_color)
    return leaf_c
    
def identifyClusters(color_list, leaves, col_list, top_color):
    fixed_colors = clusterColors(color_list, top_color)
    print fixed_colors, len(fixed_colors)
    color_dict = ddict(list)
    for color_id in range(len(leaves)):
        color = fixed_colors[color_id]
        leaf = leaves[color_id]
        col_label = col_list[leaf]
        color_dict[color].append(col_label)
    return color_dict    
    
def writeClusters(cluster_dict, output_file):
    write_file = open(output_file, 'w')
    for cluster_id in cluster_dict:
        write_file.write(cluster_id + '\n')
        for element in cluster_dict[cluster_id]:
            write_file.write('\t' + element + '\n')
    
def identifyHighCoorRows(data_matrix, row_labels, col_labels, col_id, direction):
    row_label_list = []
    for row_id in range(len(data_matrix)):
        row = data_matrix[row_id]
        interest_value = row[col_id]
        if interest_value < .01 and direction in row_labels[row_id]:
            row_label_list.append(row_labels[row_id])
    return row_label_list
    
def tcgaStandardID(col_list):
    fixed_list = [x[:12] for x in col_list]
    return fixed_list

def createCoorDict(data_matrix,row_labels,col_labels, target_list,direction = 'down'): #identifies the row entries most highly coorelated with col entries
    coorDict = {}
    col_labels = tcgaStandardID(col_labels)
    for col_id in range(len(col_labels)):
        col = col_labels[col_id]
        highCoorRows = identifyHighCoorRows(data_matrix, row_labels, col_labels, col_id, direction) 
        coorDict[col] = highCoorRows
    final_dict = {}
    for e in coorDict:
        if e in target_list:
            final_dict[e] = coorDict[e]
    return final_dict
    
def identifyCommonGenes(p_list, gmt_file, percentage_common): #a method that will identify genes with a given percentage of commonality accross a cluster
    gmt = readGMT(gmt_file)
    len_p_list = len(p_list)
    threshold = int((percentage_common/100.0)*len_p_list)
    print len_p_list, threshold
    gene_list = []
    common_genes = []
    for p in p_list:
        if p in gmt:
            gene_list.extend(gmt[p])
    print len(gene_list)
    gene_counter = Counter(gene_list)
    for gene_key in gene_counter:
        if gene_counter[gene_key] >= threshold:
            common_genes.append(gene_key)
    return common_genes

def binarizeMatrix((data_matrix,row_labels,col_labels),threshold):
    binaryMatrix = data_matrix
    for rowID in range(len(binaryMatrix)):
        for colID in range(len(binaryMatrix[rowID])):
            if binaryMatrix[rowID][colID] < threshold:
                binaryMatrix[rowID][colID] = 1
            else:
                binaryMatrix[rowID][colID] = 0
    return binaryMatrix, row_labels, col_labels 
            
