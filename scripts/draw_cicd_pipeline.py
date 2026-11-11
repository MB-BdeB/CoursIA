import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, ax = plt.subplots(figsize=(10,3))
ax.axis('off')

stages = ['Dev (Git)', 'CI (Tests/Build)', 'Container Registry', 'Staging', 'CD (Deploy)', 'Monitoring']
xs = [1,3,5,7,9,11]

for x,stage in zip(xs,stages):
    rect = patches.FancyBboxPatch((x-0.9,1.0),1.8,0.8,boxstyle='round,pad=0.3',edgecolor='black',facecolor='#fff2cc')
    ax.add_patch(rect)
    ax.text(x,1.4,stage,ha='center',va='center')

for i in range(len(xs)-1):
    ax.annotate('',xy=(xs[i+1]-0.8,1.4),xytext=(xs[i]+0.8,1.4),arrowprops=dict(arrowstyle='->',lw=1.2))

# annotations
ax.text(2,0.5,'Unit tests, linting',ha='center',fontsize=8)
ax.text(4,0.5,'Build image, GPU test',ha='center',fontsize=8)
ax.text(8,0.5,'Blue/Green or Canary',ha='center',fontsize=8)
ax.text(11,0.5,'Prometheus/Grafana alerts',ha='center',fontsize=8)

plt.tight_layout()
plt.savefig('c:/Users/Public/Documents/TELECHARGEMENT/BdeB/images/cicd_pipeline.png',dpi=150)
print('WROTE:c:/Users/Public/Documents/TELECHARGEMENT/BdeB/images/cicd_pipeline.png')
