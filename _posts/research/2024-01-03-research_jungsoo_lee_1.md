---
title: 'An Intuitive Framework to Minimize Cognitive Load in RoboticControl A Comparative Evaluation of Body Parts'
image: images/research/jungsoo_1_main.png
tags:
  - Cognitive Load Reduction
  - IMU-based Robot Control
  - Body-part Comparison

author: Jungsoo-Lee
member: Jungsoo-Lee
group: research_3

---
**Goal** 

The objective of this study is to propose an intuitive robot control framework that minimizes cognitive load by inferring user intent through a single IMU sensor, eliminating the need for complex sensor setups.


***

**Summary**

This study proposes an intuitive robot control framework aimed at minimizing cognitive load by using a single IMU sensor attached to specific body parts (wrist, torso, or head) to infer the user's motion intent. By directly utilizing raw orientation data without requiring complex calibration or multi-sensor setups, the system enables real-time, natural robot control.
A comparative evaluation shows that wrist-based control is preferred by expert users for its stability and performance, while torso-based control is favored by non-experts for its intuitiveness and ease of use. Both methods outperform traditional joystick control in usability due to their hands-free operation.
The framework’s practicality is further supported by its compatibility with common smart devices, indicating strong potential for real-world applications in human-robot interaction.

***

**Publication Link** : 
[**2024 21st International Conference on Ubiquitous Robots(UR)**](https://scholar.google.com/citations?view_op=view_citation&hl=ko&user=o7u_E8wAAAAJ&pagesize=100&citation_for_view=o7u_E8wAAAAJ:5Ul4iDaHHb8C)

{% capture col1 %}
{%
  include figure.html
  image="images/research/jungsoo_1_1.png"
  
%}
{% endcapture %}
{% capture col2 %}
{%
  include figure.html
  image="images/research/jungsoo_1_2.png"
  
%}
{% endcapture %}
{% include two-col.html col1=col1 col2=col2 %}


{%
  include figure.html
  image="images/research/jungsoo_1_3.png"
  
%}