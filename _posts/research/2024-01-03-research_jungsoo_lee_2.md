---
title: Transferable Convolutional Neural Networks for IMU-based Motion Gesture Recognition in Human-Machine Interaction
image: images/research/jungsoo_2_main.png
tags:
  - Transfer Learning
  - Hand gesture Recognition (HGR)
  - Human-Robot Interaction (HRI)
  - Convolutional Neural Networks (CNNs)

author: Jungsoo-Lee
member: Jungsoo-Lee
group: research_3

---
**Goal** 

The objective of this study is to develop an efficient and lightweight CNN model for motion gesture recognition using a single wrist-worn IMU sensor, and to explore the use of transfer learning for classifying novel gestures with limited training data, enabling more intuitive and user-friendly interaction systems.

***

**Summary**

This study proposes a lightweight Convolutional Neural Network (CNN) model designed to recognize motion-based hand gestures using raw data from a single Inertial Measurement Unit (IMU) sensor worn on the wrist. The model directly processes low-dimensional motion inputs — linear acceleration and angular velocity — and is optimized for real-time deployment on wearable devices such as smartwatches, eliminating the need for external sensors or complex preprocessing.
The research consists of two phases. In the first phase, the CNN was trained on ten predefined gestures and achieved an impressive recognition accuracy of 99.48%. In the second phase, transfer learning was employed by reusing the backbone of the pretrained network to classify four new gestures under limited training data conditions. The results showed that the transfer learning approach consistently outperformed baseline models trained from scratch, with the best accuracy reaching 95.62%, highlighting the backbone's ability to effectively extract motion-related features.
With a compact model architecture comprising only 0.12 million parameters and 0.051 GFLOPs, the proposed system is well-suited for resource-constrained environments. Additionally, experiments under various data scarcity scenarios (1:3, 1:7, 1:19 train-to-test ratios) demonstrated the model’s strong data efficiency and generalization capability, indicating reduced training overhead.
Overall, this study demonstrates that a well-structured, lightweight CNN model combined with transfer learning can enable accurate, efficient, and user-centric hand gesture recognition, paving the way for future applications in intuitive HMI systems based on wearable technologies.

***

**Publication Link** : 
[**2024 24th International Conference on Control, Automation and Systems (ICCAS)**](https://scholar.google.com/citations?view_op=view_citation&hl=ko&user=o7u_E8wAAAAJ&pagesize=100&citation_for_view=o7u_E8wAAAAJ:D_sINldO8mEC)

{% capture col1 %}
{%
  include figure.html
  image="images/research/jungsoo_2_1.png"
  
%}
{% endcapture %}
{% capture col2 %}
{%
  include figure.html
  image="images/research/jungsoo_2_2.png"
  
%}
{% endcapture %}
{% include two-col.html col1=col1 col2=col2 %}


{%
  include figure.html
  image="images/research/jungsoo_2_3.png"
  
%}