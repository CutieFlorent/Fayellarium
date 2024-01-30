# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 12:38:00 2024

@author: frank
"""

import numpy as np
from scipy.special import factorial,genlaguerre,sph_harm
from skimage.measure import marching_cubes
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

#origional wave function
def cloud(n, l, m):
    def R(r):
        factor = np.sqrt( (2/n)**3 *\
            factorial(n-l-1) / (2*n*factorial(n+l)))
        rho = 2*r/n
        return factor * rho**l *np.exp(-rho/2)*\
            genlaguerre(n-l-1, 2*l+1)(rho)
    def Y(th,ph):
        return sph_harm(m, l, ph, th)
    return lambda r,th,ph: R(r) * Y(th,ph)
def spdf(n, l,):
    size = 2*l+1
    bases = np.array(
        [[cloud(n,l,m)(R,TH,PH) for m in range(-l,l+1)]])
    M = np.zeros((size,size),dtype=complex)
    a,b = np.indices(M.shape)
    M[np.where(a==b)] = 1j
    M[np.where(a+b==size-1)] = 1j
    M[np.where((M!=0) & (a>=l))] = 1 
    M[np.where((M!=0) & (b>l) & (a<l) & ((a-l)%2==0))] = -1j
    M[np.where((M!=0) & (b>l) & (a>l) & ((a-l)%2==1))] = -1
    M /= np.sqrt(2)
    res = ((M @ bases.T).T)[0]
    return [res[i-l-1] for i,_ in enumerate(res)]
    
    
    
    
#environment settings
limit = 128
resol = 100
prob_f = 0.02

step = 2*limit / (resol-1)
#coordinates
vec = np.linspace(-limit, limit,resol)
X, Y, Z = np.meshgrid(vec,vec,vec)
R = np.sqrt(X**2+Y**2+Z**2)
TH = np.arccos(Z/R)
PH = np.arctan2(Y,X)
#create model
def model(ps,total=False):
    value = ps(R,TH,PH) if callable(ps) else ps
    dens = np.abs(value)**2
    a,b,c = np.indices(dens.shape)
    dens[np.where((a>resol/2) & (b>resol/2))] = 0 #slice#
    dens_p = np.where(value>0,dens,0)
    dens_n = np.where(value<0,dens,0)
    prob = prob_f*np.max(dens)
    def verts_faces(dens):
        verts,faces,_,_ = marching_cubes(
            dens,level=prob,spacing=(step,step,step))
        verts -= 1*limit
        verts[:,[0,1]] = verts[:,[1,0]]
        return verts,faces
    pos = verts_faces(dens_p)
    neg = verts_faces(dens_n)
    if total: return verts_faces(dens)
    return pos,neg
    
#fig and ax
def fig_ax(plot_range=limit):
    fig = plt.figure(dpi=256)
    ax = fig.add_subplot(1, 1, 1, projection="3d")
    ax.set_box_aspect([1, 1, 1])
    ax.view_init(elev=30, azim=30)
    
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    ax.set_zlabel("$z$")

    ax.set_xlim(-plot_range, plot_range)
    ax.set_ylim(-plot_range, plot_range)
    ax.set_zlim(-plot_range, plot_range)
    
    ticks = np.linspace(-plot_range, plot_range, 9)
    ax.set_xticks(ticks)
    ax.set_yticks(ticks)
    ax.set_zticks(ticks)
    #print(fig,ax)
    return fig, ax

fig, ax = fig_ax()
def draw_model(ps):
    pos,neg=model(ps)
    def add_model(m,color):
        verts,faces=m
        mesh = Poly3DCollection(verts[faces], lw=0.05) 
        mesh.set_facecolor(color)
        mesh.set_edgecolor("black")
        ax.add_collection3d(mesh)
    add_model(pos,'cyan')
    add_model(neg,'pink')
    #print(mesh)
    #plt.show()
    #return mesh,verts,faces
def draw_model_total(ps):
    verts,faces=model(ps,total=True)
    mesh = Poly3DCollection(verts[faces], lw=0.05) 
    mesh.set_facecolor('yellow')
    mesh.set_edgecolor("black")
    ax.add_collection3d(mesh)
def blender_model(ps,name):
    filename = name+".obj"
    with open(filename, "w") as f:
        pass
    m = model(ps,total=True)
    def add_model(m,name):
        verts,faces =m
        with open(filename, "a") as f:
            f.write(f"o {name} {resol}\n")
            for vert_coords in verts:
                x, y, z = vert_coords
                f.write("v %s %s %s \n" % (x, y, z))
            for vert_ids in faces:
                id_1, id_2, id_3 = vert_ids + 1
                f.write("f %s %s %s \n" % (id_1, id_2, id_3))
    #add_model(pos,'pos')
    #add_model(neg,'neg')
    add_model(m,'orbital')
            
pass
#draw_model((1j*cloud(5,4,2)(R,TH,PH)-1j*cloud(5,4,-2)(R,TH,PH)))
#draw_model(spdf(10,8)[3])
#blender_model(cloud(4,1,0),'4p')

#sp_bases = np.array([sp_bases])
#sp3M=np.array([[1,1,1,1],
              #[1,1,-1,-1],
              #[1,-1,1,-1],
              #[1,-1,-1,1]])/2
#sp3_bases = np.array([np.concatenate([spdf(6,0),spdf(6,1)])])
#sp3_cloud = ((sp3M @ sp3_bases.T).T)[0]
#draw_model(spdf(2,0)[0]+spdf(2,1)[0]+spdf(2,1)[1]+spdf(2,1)[2])
#draw_model(sp3_cloud[0])
#d=spdf(4,3)
#+spdf(3,1)[0]+spdf(3,1)[-1]+\spdf(3,1)[1]+
#sp3d2 = np.sqrt(1/6)*spdf(4,0)[0]-\
        #np.sqrt(1/2)*spdf(4,1)[0]+\
        #np.sqrt(1/3)*spdf(4,2)[0]
        

#alt_d = np.sqrt(1/7)*d[0]+np.sqrt(2/7)*d[1]+np.sqrt(2/7)*d[-2]+np.sqrt(2/7)*d[3]
#draw_model(sp3_cloud[3])
draw_model_total(cloud(8,6,3))
plt.show()




















