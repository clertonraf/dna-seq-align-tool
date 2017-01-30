################################################################################
# 
#       file:   align.py  
#       author: Clerton Ribeiro 
#  
#
#       Contact: craf@cin.ufpe.br
#
#	Script que calcula alimento global, semiglobal e local de duas
#	sequencias, com as respectivas restricoes de Match,Insercao,Substituicao
#	e Remocao.
#
#
################################################################################ 
import optparse

def readInput(input_data):
	"""
	Metodo que le a entrada de dados

        @param input_data: caminho do arquivo a ser usado na entrada de dados
            
        @return: s,t,align_type,parameters,prior
	"""
	file_input = open(input_data,"r")
	s = file_input.readline()
	s = s.replace("\n","")
	
	t = file_input.readline()
	t = t.replace("\n","")

	align_type = file_input.readline()
	align_type = align_type.replace("\n","")

	parameters = file_input.readline()
	parameters = parameters.replace("\n","")
	parameters = parameters.split(" ")

	prior = file_input.readline()
	prior = prior.replace("\n","")
	prior = prior.split(" ")

	return s,t,align_type,parameters,prior

def createMatrix(s,t):
	"""
	Metodo que cria as matrizes usadas para guardar os passos do algoritmo.

        @param s: primeira sequencia a ser comparada
	@param t: segunda sequencia a ser comparada        
	    
        @return: m,n,matrix,traceback

	"""
	m = len(s)
	n = len(t)

	matrix = [[0 for col in range(m+1)] for row in range(n+1)]
	traceback = [[0 for col in range(m+1)] for row in range(n+1)]
	
	return m,n,matrix,traceback


def initializeMatrix(matrix,m,n,parameters,align_type,debug=False):
	"""
	Metodo responsavel pela inicializacao das matrizes.

	Todas as matrizes sao inicializadas com dimensao nxm e com valores iniciais
	zeros para todas as posicoes.

	Para o alinhamento global, a inicializacao e diferente, pois sao consideradas 
	as penalidades para remocao.

        @param matrix: a matriz para calculo do score de cada sequencia  
	@param m: tamanho da primeira sequencia
	@param n: tamanho da segunda sequencia
	@param parameters: lista com os valores das penalidades para Match, Insercao, Substituicao e remocao
	@param align_type: tipo de alinhamento (global, semiglobal ou local)
	@param debug: default 0. Escolher 1 para imprimir passos do algoritmo       
	    
        @return: matrix

	"""

	if align_type == 'global':
	
		for index in range(0,m+1):
			matrix[0][index] = index*int(parameters[2])

		for index in range(0,n+1):
			matrix[index][0] = index*int(parameters[3])
		
		if debug == 1:
			print "\nMatrix initialization\n"
			for i in matrix:
				print i			
		return matrix	
	else:
		if debug == True:
			print "\nMatrix initialization\n"
			for i in matrix:
				print i	
		return matrix

def fillMatrix(matrix,traceback,m,n,parameters,align_type,debug=False):
	"""
	Metodo responsavel pelo preenchimento das matrizes.

	O preenchimento e similar aos alinhamentos global, semiglobal e local.
	a diferenca esta no alinhamento local, em que uma quarta alternativa
	para o preenchimento e considerada: o zero.

        @param matrix: a matriz para calculo do score de cada sequencia
	@param traceback: a matriz com o registro da procedencia de cada score  
	@param m: tamanho da primeira sequencia
	@param n: tamanho da segunda sequencia
	@param parameters: lista com os valores das penalidades para Match, Insercao, Substituicao e remocao
	@param align_type: tipo de alinhamento (global, semiglobal ou local)
	@param debug: default 0. Escolher 1 para imprimir passos do algoritmo       
	    
        @return: matrix, traceback

	"""
	for i in range(1,n+1):
		for j in range(1,m+1):
			left = matrix[i][j-1] + int(parameters[2])
			top = matrix[i-1][j] + int(parameters[3])
			penalty = 0
			if s[j-1] == t[i-1]:
				penalty = int(parameters[0])
			else:
				penalty = int(parameters[1])
			both = matrix[i-1][j-1]+penalty
		
			best = left
			path = -1
			if top > best:
				best = top
				path = 1
			if both > best:
				best = both
				path = 0
			if align_type == 'local':
				if 0 > best:
					best = 0
			matrix[i][j] = best
			traceback[i][j] = path
	if debug==True:

		print "\nMatrix filled\n"
		for row in matrix:
			print row

		print "\nTraceback matrix\n"
		for row in traceback:
			print row
					
	return matrix,traceback

def computeAlignment(matrix,traceback,m,n,align_type,debug=False):
	"""
	Metodo que faz o backtracking construindo o alinhamento final
	
	A matriz informando de onde foi calculada o resultado da celula e usada
	para a computacao final do alinhamento das sequencias. 

	Para os alinhamentos local e semiglobal, o processo de construcao do alinhamento
	pode nao se iniciar na celula mais a direita-inferior da matriz, portanto, e necessario
	localizar a melhor posicao para iniciar o processo. A diferenca em relacao a dimensao
	da matriz e considerada como um gap.

        @param matrix: a matriz para calculo do score de cada sequencia
	@param traceback: a matriz com o registro da procedencia de cada score    
	@param m: tamanho da primeira sequencia
	@param n: tamanho da segunda sequencia
	@param parameters: lista com os valores das penalidades para Match, Insercao, Substituicao e remocao
	@param align_type: tipo de alinhamento (global, semiglobal ou local)
	@param debug: default 0. Escolher 1 para imprimir passos do algoritmo       
	    
        @return: matrix
	
	"""

	i = n
	j = m
	result = []
	
	if (align_type == 'local') or (align_type == 'semiglobal'):
		best = matrix[0][0]
		for k in range(0,n+1):
			for l in range(0,m+1):
				if matrix[k][l] > best:
					best = matrix[k][l]
					i = k
					j = l

		if i < n:
			result.append((n-i)*'-')
		if j < m:
			result.append((m-j)*'-')
	if debug == True:
		print "\nFilled matrix\n"
		for row in matrix:
			print row
		print "\nInicial position: matrix["+str(i)+"]["+str(j)+"]\n"
	
	while i > 0 and j > 0 :
		if traceback[i][j] == 0:
			if align_type == 'local' and matrix[i][j] == 0:
				break
			result.append(s[j-1])
			i-=1
			j-=1		
		elif(traceback[i][j] == 1):
			result.append("-")
			i-=1
		elif(traceback[i][j] == -1):
			result.append("-")
			j-=1
		else:
			print "error"
	if i > 0:
		result.append(i*'-')
	if j > 0:
		result.append(j*'-')
	result = "".join(result)
	return result[::-1]

usage = "Usage: %prog [options] arg1 arg2...\nTry %prog -h or %prog --help to see the available options"
parser = optparse.OptionParser(usage)
parser.add_option('-f', '--file', type="string", dest="filename", default=None, help="Path to datafile")
parser.add_option('-v','--verbose', action="store_true", dest="verbose", default=False)
options, args = parser.parse_args()
filename = options.filename

s,t,align_type,parameters,prior = readInput(filename)

print "\nEntrada\n"
print s
print t
print align_type
print parameters
print prior

m,n,matrix,traceback = createMatrix(s,t)

matrix = initializeMatrix(matrix,m,n,parameters,align_type)

matrix,traceback = fillMatrix(matrix,traceback,m,n,parameters,align_type,options.verbose)

result = computeAlignment(matrix,traceback,m,n,align_type,options.verbose)

print "\nAlinhamento",align_type,"\n"
print result