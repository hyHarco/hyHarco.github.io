---
title: Multitask Learning for Multiple Recognition Tasks in Lower-limb Exoskeleton robot
image: images/jh_research_model_structure.png
tags:
  - Lower-Limb Exoskeleton Robot
  - Multitask Learning
  - Few-Shot Learning
author: Joonhyun Kim
member: Joonhyun-Kim
group: research_1
---
**Goal** : This study shows that Gait Phase Recognition (GRP) and Terrain Classification (TC), the most conventional Recognition Tasks of Lower-limb Exoskeleton robots, can be effectively solved by introducing a Multi-task Learning.

***

**Summary**
Multi-task learning, (or Transfer learning), is a concept derived from the field of computer vision, and is a learning method that enables better performances and data-efficient learning when learning is conducted by sharing a Feature Network (encoder) for related tasks.   
   
Researcher [*Joon-hyun Kim*](http://harco.hanyang.ac.kr/members/Joonhyun-Kim.html) developed a model that predict Gait Phase Recognition (GRP) and Terrain Classification (TC), the most conventional Recognition Tasks of Lower-limb Exoskeleton robots, based on theses Multitask Learning Framework idea.
    
He first created a high-performing GPR model that achieved a Root mean square error (RMSE) value of 2.345 ±0.08 and then utilized its knowledge-sharing backbone
feature network to learn a TC model with an extremely limited dataset. 
Using a limited dataset for the TC model allows us to validate the data efficiency of our proposed Multitask learning
approach. He compared the accuracy of the proposed TC model against other TC baseline models. The proposed model achieved
99.5 ±0.044% accuracy with a limited dataset, outperforming other baseline models, demonstrating its effectiveness in terms of data efficiency.

***

**Topic**    
 * Recognition Problems in Lower-limb Exoskeleton Robot
 * Few-Shot Learning
 * Multitask Learning


   
   
***
**Conference**   
- [**_kspe (Korean Society for Precision Engineering) Conference_**](https://www.dbpia.co.kr/journal/articleDetail?nodeId=NODE11168452)
- [**_IEEE ROMAN 2023_**](https://ro-man2023.org/main) (Acceted, Announcement scheduled for August 28)

***



**<i class="fas fa-play-circle"></i> Video**

Multitask Model Online Test Video to simultaneously Re
ognize Gait Phase and Terrrain
<iframe width="560" height="315" src="https://www.youtube.com/embed/vQQiFxAiJ_w" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>



{%
  include figure.html
  image="images/jh_research_inputpipelining.png"
  caption="Input Pipelining Algorithm"
  width="80%"
%}

{%
  include figure.html
  image="images/jh_research_model_structure.png"
  caption="Multitask Model Structure"
  width="80%"
%}


{% capture col1 %}
{%
  include figure.html
  image="images/jh_research_sensor.png"
  caption="Data Collecting Sensors"
%}
{% endcapture %}
{% capture col2 %}
{%
  include figure.html
  image="images/jh_research_terrain_img.png"
  caption="Illustration of the terrains used in our experiments, and Data collected on a 35m long
flat surface and a 4.2m long staircase with a 29.05°angle."
%}
{% endcapture %}
{% include two-col.html col1=col1 col2=col2 %}




***
**related project** 
- [**_Development of Solution Technology for Personalized Gait Control and Performance Evaluation of Lower-limb Robotic Exoskeleton through Artificial Intelligence/Big Data_**](http://harco.hanyang.ac.kr/2022/04/28/project-voucher_iitp_gait_project.html)