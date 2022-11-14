---
title: Development of the IMU Based GAIT Phase Prediction Model using CNN Model
image: images/jh_research1.png
tags:
  - GAIT Phase
  - Convolutional Neural Network
author: Joonhyun Kim
member: Joonhyun-Kim
group: research_1
---
**Goal** : This study predicts GAIT Phase, which shows strong performance in terrain and speed change.

***

**Summary**
Convolutional Neural Network(CNN) is a widely used model in the field of Computer Vision, an artificial neural network model that captures characteristic changes in data through convolutional filters and performs various predictions.    

Researcher [*Joon-hyun Kim*](http://harco.hanyang.ac.kr/members/Joonhyun-Kim.html) developed a model that predicts the GAIT phase of exoskeleton robot wearer using CNN.
    
When he created the model, he organized the data collection environment into various terrain (Level Ground Walk, Stair Ascent, Stair Descent) and various speeds (70-130 bpm) to make the model strong in various environmental changes.

***

**Topic**    
 * GAIT Phase
 * Convolutional Neural Network


***
**related project** 
- [**_Development of Solution Technology for Personalized Gait Control and Performance Evaluation of Lower-limb Robotic Exoskeleton through Artificial Intelligence/Big Data_**](http://harco.hanyang.ac.kr/2022/04/28/project-voucher_iitp_gait_project.html)   
   
***
**Conference**   
- 
[**_kspe (Korean Society for Precision Engineering) Conference_**](https://drive.google.com/file/d/1p5hMve-M4tQ8fD1xHreyuUOgk3CVtTga/view)


***


{%
  include figure.html
  image="images/jh_research1.png"
  caption="CNN Filtering"
%}


{% capture col1 %}
{%
  include figure.html
  image="images/P_NEWS/daegu_exco_kspe.png"
  caption="KSPE Conference Presentation"
%}
{% endcapture %}
{% capture col2 %}
{%
  include figure.html
  image="images/voucher_data_collecting.png"
  caption="Various terratin / Speed Data Collecting"
%}
{% endcapture %}
{% include two-col.html col1=col1 col2=col2 %}




