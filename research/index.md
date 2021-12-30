---
title: Research
nav:
  order: 1
  tooltip: research landscape
---

# <i class="fas fa-microscope"></i>Research

Deep learning is not easy. For example, applying deep learning on a specifcal microscopy image analysis problem is much more than collecting images, making annotations, and feeding the images with annotations into a neural network. On one hand, annotation is not easy and sometimes even impossible (e.g., accurately annotating the segmentation of a very complex shape in 3D is nearly impossible). On the other hand, there are many important questions to think about. How to evaluate the quality of your annotation? What if different people have different annotations? How can I annotate the minimal amount of data to achieve to desired accuracy? When I apply my model on new images, how do I know the results are correct? ... 

Solving real computational biomedical problems with AI is not straightforward. The quantitative tasks in many biomedical applications may not be easily formulated into common deep learning or computer vision problems (e.g., segmentation, classification, image reconstruction, etc.). Even a well-defined problem, we may face very different challenges in the specific biomedical context than the problem's original general computer vision setting. For example, it would be easy for everyone to accuratly annotate the contour of a car in a 2D image, but it could be very difficult to annotate the boundary of a nucleus in a 3D confocal microscopy image. It is not only because 3D is hard, but also because you have to take the diffraction of light into account to avoid over-segmentation. Or, minor segmentation error of cars may not be a big deal, but minor segmentation error of nuclei (e.g., over-smoothed boundary of nuclei with complex shape when being squeezed) may yield very different biomedical findings. So, to develop a successful AI-based microscopy image analysis algorithm, it is very important to have good understanding of microscopy and the underlying biomedical application.

Please also check out our blog posts on [basic machine vision concepts](https://mmv-lab.github.io/blog/?search=%22tag:basic%20concepts%22), such as [semantic segmentation](https://mmv-lab.github.io/blog/?search=%22tag:semantic%20segmentation%22), [instance segmentation](https://mmv-lab.github.io/blog/?search=%22tag:instance%20segmentation%22), [object detection](https://mmv-lab.github.io/blog/?search=%22tag:object%20detection%22), [image to image transfer](https://mmv-lab.github.io/blog/?search=%22tag:image2image%20transfer%22), etc.

{% include section.html %}

{% include search-box.html %}

{% include search-info.html %}

{% include list.html data="citations" component="citation" style="rich" %}
