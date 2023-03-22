
from DynamicMarkovBlanketDiscovery import *

f = r"c://Users/brain/Desktop/movie_temp.mp4"
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
from matplotlib import cm 

print('Test on Newtons Cradle Data')
from NewtonsCradle import NewtonsCradle
dmodel = NewtonsCradle(n_balls=5,ball_size=0.2,Tmax=1000,batch_size=20,g=1,leak=0.05/8,dt=0.05) 

# data_temp = dmodel.generate_data('random')[0]
# data_temp = data_temp[0::5]
# data = data_temp

data_temp = dmodel.generate_data('1 + 1 ball object')[0]
data_temp = data_temp[0::5]
data = data_temp
#data = torch.cat((data,data_temp),dim=1)

data_temp = dmodel.generate_data('1 ball object')[0]
data_temp = data_temp[0::5]
data = torch.cat((data,data_temp),dim=1)

# data_temp = dmodel.generate_data('2 ball object')[0]
# data_temp = data_temp[0::5]
# data = torch.cat((data,data_temp),dim=1)

# data_temp = dmodel.generate_data('3 ball object')[0]
# data_temp = data_temp[0::5]
# data = torch.cat((data,data_temp),dim=1)

# data_temp = dmodel.generate_data('2 + 2 ball object')[0]
# data_temp = data_temp[0::5]
# data = torch.cat((data,data_temp),dim=1)

# data_temp = dmodel.generate_data('4 ball object')[0]
# data_temp = data_temp[0::5]
# data = torch.cat((data,data_temp),dim=1)



v_data = torch.diff(data,dim=0)
data = data[1:]
data = torch.cat((data,v_data),dim=-1)

model = DMBD(obs_shape=data.shape[-2:],role_dims=(4,4,4),hidden_dims=(2,2,2),batch_shape=(),regression_dim = 0, control_dim=0)
v_model = DMBD(obs_shape=v_data.shape[-2:],role_dims=(4,4,4),hidden_dims=(2,2,2),regression_dim = 0, control_dim=0)

model.update(data,None,None,iters=20,latent_iters=1,lr=0.5)
model.update(data,None,None,iters=20,latent_iters=1,lr=1)
print('Generating Movie...')
f = r"c://Users/brain/Desktop/cradle.mp4"
ar = animate_results('sbz',f, xlim = (-1.6,1.6), ylim = (-1.2,0.2), fps=10)
ar.make_movie(model, data, (10,30))

sbz=model.px.mean()
B = model.obs_model.obs_dist.mean()
if model.regression_dim==0:
    roles = B@sbz
else:
    roles = B[...,:-1]@sbz + B[...,-1:]
sbz = sbz.squeeze()
roles = roles.squeeze()
batch_num = 41
idx = model.obs_model.NA/model.obs_model.NA.sum()>0.001
plt.plot(roles[:,batch_num,:,0],roles[:,batch_num,:,1])
plt.show()
plt.plot(roles[:,batch_num,:,2],roles[:,batch_num,:,3])
plt.show()

stop

v_model.update(v_data,None,None,iters=20,latent_iters=1,lr=0.5)
v_model.update(v_data,None,None,iters=20,latent_iters=1,lr=1.0)
print('Generating Movie...')
f = r"c://Users/brain/Desktop/cradle_v.mp4"
ar = animate_results('sbz',f,xlim = (-1.6,1.6), ylim = (-1.2,0.2), fps=10)
ar.make_movie(v_model, data, (10,30,50,70))

sbz=v_model.px.mean()
B = v_model.obs_model.obs_dist.mean()
if v_model.regression_dim==0:
    roles = B@sbz
else:
    roles = B[...,:-1]@sbz + B[...,-1:]
sbz = sbz.squeeze()
roles = roles.squeeze()
batch_num = 51

idx = model.obs_model.NA/model.obs_model.NA.sum()>0.001

plt.plot(roles[:,batch_num,:,0],roles[:,batch_num,:,1])
plt.show()
# print('Test on life as we know it data set')

# y_data=np.genfromtxt('ly.txt')
# x_data=np.genfromtxt('lx.txt')
# y=torch.tensor(y_data,requires_grad=False).float()
# x=torch.tensor(x_data,requires_grad=False).float()
# y=y.unsqueeze(-1)
# x=x.unsqueeze(-1)
# data = torch.cat((x,y),dim=-1)
# data = data.transpose(0,1).unsqueeze(1)
# data = data[1000:]
# data = data/data.std()
# data = data - data.mean()

# v_data = torch.diff(data,dim=0)
# v_data = v_data/v_data.std()
# data = data[1:]
# data = torch.cat((data,v_data),dim=-1)


# # print('Initializing V model....')
# # v_model = DMBD(obs_shape=v_data.shape[-2:],role_dims=(20,20,20),hidden_dims=(4,4,4,2))
# # print('Updating model V....')
# # v_model.update(v_data,None,None,iters=50,latent_iters=1,lr=1.0)
# # #v_model.update(v_data,None,None,iters=10,latent_iters=1,lr=1)
# # print('Done')
# # f = r"c://Users/brain/Desktop/wil_v.mp4"
# # ar = animate_results('sbz',f)
# # ar.make_movie(v_model, data, 0)

# print('Initializing X + V model....')
# model = DMBD(obs_shape=data.shape[-2:],role_dims=(12,8,4),hidden_dims=(6,4,2,2))
# print('Updating model X+V....')
# model.update(data,None,None,iters=50,latent_iters=1,lr=0.8)
# #model.update(data,None,None,iters=10,latent_iters=1,lr=1)
# print('Done')
# f = r"c://Users/brain/Desktop/wil.mp4"
# ar = animate_results('role',f)
# ar.make_movie(model, data, 0)
# sbz=model.px.mean()
# B = model.obs_model.obs_dist.mean()
# roles = B[...,:-1]@sbz + B[...,-1:]
# sbz = sbz.squeeze()
# roles = roles.squeeze()[...,0:2]

# plt.plot(roles[:,:,0],roles[:,:,1])






# print('Test on Artificial Life Data')
# print('Loading data....')
# y_data=np.genfromtxt('rotor_story_y.txt')
# x_data=np.genfromtxt('rotor_story_x.txt')
# y=torch.tensor(y_data,requires_grad=False).float()
# x=torch.tensor(x_data,requires_grad=False).float()
# y=y.unsqueeze(-1)
# x=x.unsqueeze(-1)

# T = 100
# data = torch.cat((y,x),dim=-1)
# data = data[::10]
# v_data = torch.diff(data,dim=0)
# v_data = v_data/v_data.std()
# data = data[1:]
# #start = data.shape[0]%T
# #data = data[start:]
# #v_data = v_data[start:]



# #num_samples = data.shape[0]
# #data = torch.reshape(data.unsqueeze(0),(num_samples//T,T,200,2)).float().swapaxes(0,1)
# #v_data = torch.reshape(v_data.unsqueeze(0),(num_samples//T,T,200,2)).float().swapaxes(0,1)
# data = data.unsqueeze(1)
# v_data = v_data.unsqueeze(1)


# data = data/data.std()
# v_data = v_data/v_data.std()

# data = torch.cat((data,v_data),dim=-1)
# # #profile = torch.profiler.profile()

# # print('Initializing V model....')
# # v_model = DMBD(obs_shape=v_data.shape[-2:],role_dims=(16,16,16),hidden_dims=(3,3,3))
# # print('Updating model V....')
# # v_model.update(v_data,None,None,iters=50,latent_iters=1,lr=0.75)
# # v_model.update(v_data,None,None,iters=10,latent_iters=1,lr=1)
# # print('Done')
# # f = r"c://Users/brain/Desktop/rotator_movie_v.mp4"
# # ar = animate_results('sbz',f)
# # ar.make_movie(v_model, data, 0)

# print('Initializing X + V model....')
# model = DMBD(obs_shape=data.shape[-2:],role_dims=(50,0,0),hidden_dims=(20,0,0,2))


# print('Updating model X+V....')
# model.update(data,None,None,iters=100,latent_iters=1,lr=0.25)
# #model.update(data,None,None,iters=10,latent_iters=1,lr=1)
# print('Done')
# f = r"C://Users/brain/Desktop/rotator_movie.mp4"
# ar = animate_results('role',f)
# ar.make_movie(model, data, 0)

# sbz=model.px.mean()
# B = model.obs_model.obs_dist.mean()
# roles = B[...,:-1]@sbz + B[...,-1:]
# sbz = sbz.squeeze()
# roles = roles.squeeze()[...,0:2]

# plt.plot(roles[:,:,0],roles[:,:,1])
