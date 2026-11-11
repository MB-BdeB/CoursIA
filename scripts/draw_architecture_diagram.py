import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, ax = plt.subplots(figsize=(10,6))
ax.set_xlim(0,10)
ax.set_ylim(0,6)
ax.axis('off')

# Draw CPU
cpu = patches.FancyBboxPatch((0.5,3.8),2,1,boxstyle='round,pad=0.3',edgecolor='black',facecolor='#cfe2f3')
ax.add_patch(cpu)
ax.text(1.5,4.3,'CPU\n8-32 cores',ha='center',va='center',fontsize=10)

# Draw PCIe bus
ax.plot([2.5,7.5],[4.3,4.3],color='black',linewidth=2)
ax.text(5,4.5,'PCIe Gen4 bus (x16 lanes)',ha='center',va='bottom')

# Draw GPUs
gpu_x = [3.0,5.0,7.0]
for i,x in enumerate(gpu_x):
    rect = patches.FancyBboxPatch((x-0.6,2.2),1.2,0.8,boxstyle='round,pad=0.2',edgecolor='black',facecolor='#f4cccc')
    ax.add_patch(rect)
    ax.text(x,2.6,f'GPU{i+1}\nRTX 4090\n24 GB',ha='center',va='center',fontsize=9)
    ax.plot([x,5.0],[3.0,3.8],color='black',linestyle='--',linewidth=1)

# NVLink annotation
ax.text(5,2.0,'NVLink (optionnel pour multi-GPU haute bande passante)',ha='center',fontsize=8)

# Storage
storage = patches.FancyBboxPatch((0.5,0.5),2,0.8,boxstyle='round,pad=0.3',edgecolor='black',facecolor='#d9ead3')
ax.add_patch(storage)
ax.text(1.5,0.9,'NVMe Storage\nDatasets / Checkpoints',ha='center',va='center',fontsize=9)

# Monitoring stack
prom = patches.FancyBboxPatch((7.5,0.5),2,1.2,boxstyle='round,pad=0.3',edgecolor='black',facecolor='#fff2cc')
ax.add_patch(prom)
ax.text(8.5,1.1,'Prometheus\nGrafana\nAlertmanager',ha='center',va='center',fontsize=9)
ax.arrow(5,2.2,3.0,-0.6,head_width=0.05,head_length=0.1,length_includes_head=True)

# Title
ax.text(5,5.6,'Architecture simplifiée d\'un écosystème IA (CPU, PCIe, GPUs, stockage, monitoring)',ha='center',fontsize=11,weight='bold')

plt.tight_layout()
plt.savefig('c:/Users/Public/Documents/TELECHARGEMENT/BdeB/images/architecture.png',dpi=150)
print('WROTE:c:/Users/Public/Documents/TELECHARGEMENT/BdeB/images/architecture.png')
