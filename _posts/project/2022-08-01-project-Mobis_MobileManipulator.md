---
title: Hyundai Mobis Mobile Manipulator Whole Body Control
mintitle: Mobile Manipulator Whole Body Control
image: images/mobis_project.png
group: ongoing  # Use filter tags as 'ongoing', 'past', 'etc'
tags:
  - PROJECT
  - Ergonomics
  - Mobile-manipulator
  - Cooperative-Robot
fund: Hyundai Mobis
date_start: 2022-08-01
date_end: 2024-04-30
role: Coordinator
budget: 240,000,000 won
---
**<i class="fas fa-sync"></i> Period : 2022-08-01 ~ 2024-04-30**   
**<i class="fas fa-won-sign"></i> Total Budget : 240,000,000 원**     


***   
#### <i class="fas fa-edit"></i>  **Goal of This Project**
* Development the of Whole Body Mobile Manipulator Control Algorithm

***    
#### <i class="far fa-edit"></i>  **Project Contents**   

**_Whole-body control of mobile manipulator for dynamic stability implementation_**    
- Corner module-based mobile manipulator (manipulator 6 degrees of freedom , mobile 12 degrees of freedom)
- hole body optimal control  framework using the redundancy of mobile manipulator to perform multitasks 
- Control to mitigate impact in case of contact with environment


**_Task configuration techniques for implementing Environment adaptability_**
- Task priority determination algorithms that change the robot’s task priorities according to human willingness to work or changes in the environment

{%
  include figure.html
  image="images/mobis_project_1.png"
%}
**_demo Scenario_**

{% capture col1 %}
{%
  include figure.html
  image="images/mobis_project_2.png"
  caption="Scenario 1) Reliable transport of loaded or gripped objects, even in unstructured terrain (e.g., slope, fine ground, etc.). Also, avoid collisions with the environment during transport and generate motion to stably transport objects in the event of a collision."
%}
{% endcapture %}
{% capture col2 %}
{%
  include figure.html
  image="images/mobis_project_3.png"
  caption = "Scenario 2) If the mobile robot cannot access the target due to the surrounding environment, the system is stabilized by Whole Body control using the robot's Redundancy while grasping the target."
%}
{% endcapture %}
{% include two-col.html col1=col1 col2=col2 %}  

***    
#### **<i class="fas fa-user-circle"></i> Participating Researchers**
* [**Wansoo Kim**](http://harco.hanyang.ac.kr/members/Wansoo-Kim.html)   : **_Principal Investigator_**  
* [**Joonkyu No**](http://harco.hanyang.ac.kr/members/Joonkyu-No.html)   :    *(S/W) Mobile Robot Control*
* [**Jaepil Jang**](http://harco.hanyang.ac.kr/members/Jaepil-Jang.html)   :   *(S/W) Whole Body Control, Task Planning*
* [**Seungmin Choi**](http://harco.hanyang.ac.kr/members/Seungmin-Choi.html)   :   *(S/W) Whole Body Control, Task Planning*

***

#### **<i class="fas fa-money-bill-wave-alt"></i> Funding**
{%
  include feature.html
  image="images/mobis_support.png"
  link='https://www.mobis.co.kr/kr/index.do'
%}   
***   