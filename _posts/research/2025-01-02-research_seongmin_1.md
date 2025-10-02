---
title:  'Pelvic IMU-Based Gait Phase Classification using Kernel-Embedded Extreme Learning Machine'
image: images/research/seongmin_1_main.png
tags:
  - Gait Phase Classification
  - Symmetric Positive Definite(SPD) Manifold
  - Extreme Learning Machine(ELM)

author: Seongmin-Ha
member: Seongmin-Ha
group: research_1
---
**Goal** :  The primary goal is to design and validate a geometry-aware gait phase classification framework capable of real-time operation with only a single pelvic inertial measurement unit (IMU). By employing Symmetric Positive Definite (SPD) covariance representations, Gaussian kernel embeddings, and a lightweight Extreme Learning Machine (ELM) classifier, the framework seeks to achieve efficient and accurate recognition of bilateral gait dynamics. The long-term aim is to provide a practical foundation for wearable systems that monitor and support hemiplegic gait in rehabilitation and assistive robotics

***

**Summary**
The proposed framework introduces a minimal-sensor gait phase classification system that relies on a single IMU positioned at the pelvis, a location well suited to capturing bilateral locomotion dynamics while minimizing setup complexity. IMU signals are transformed into SPD covariance matrices, mapped into a nonlinear feature space through Gaussian kernels, and classified using an ELM-based model. The system identifies three functional gait states—left stance with right swing, right stance with left swing, and double stance—which are especially relevant for hemiplegic gait analysis. Validation experiments with healthy participants demonstrated high accuracy (average 89.18% with Log-Euclidean distance), confirming the feasibility of accurate gait recognition without extensive sensor arrays. These findings point toward promising applications in wearable exoskeletons and rehabilitation technologies, where simplicity, responsiveness, and user comfort are essential.

***

{% capture col1 %}
{%
  include figure.html
  image="images/research/seongmin_1_1.png"
  
%}
{% endcapture %}
{% capture col2 %}
{%
  include figure.html
  image="images/research/seongmin_1_2.png"
  
%}
{% endcapture %}
{% include two-col.html col1=col1 col2=col2 %}

{%
  include figure.html
  image="images/research/seongmin_1_main.png"
%}
