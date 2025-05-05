import pickle

F = open(r'/Code Repositories/NVPDP_NIS_LiYang/NIS-datasets/pdp_100.pkl', 'rb')

content = pickle.load(F)

print(content)