---
title: Development Service of Systemic Control Algorithm for Development of Safety Guidelines for Mobile Cooperative Robot Workshop
mintitle : Safety Guidelines for Mobile Cooperative Robot Workshop
image: images/project/dgist_image.png
group: past 
tags: 
  - Human Robot Collaborate
  - Mobile Manipulator
fund: DGIST
date_start: 2022.07.15
date_end: 2022.10.13
role: Coordinator
# budget: 20,000,000 won
---

***    
**<i class="fas fa-sync"></i> Period : 2022.07.15 ~ 2022.10.13**   
<!-- **<i class="fas fa-won-sign"></i> Total Budget : 20,000,000 원**     -->

***     
#### <i class="fas fa-edit"></i>  **Goal of This Project**
* Although it is a safe enough cooperative robot, there is no difference from the function of a fixed cooperative robot because the cooperative robot attached to the mobile robot cannot be operated while on the move. Therefore, there is a problem that the efficiency of use is significantly reduced by applying the same regulations as industrial robots for work during the installation and movement of the robot.   

* Although mobile cooperative robots must perform tasks on the move, such as transportation between processes and intermediate work, collaboration between workers and mobile cooperative robots in logistics warehouses, and collaboration of many cooperative robots, existing regulations prohibit the operation of these robots.

* The purpose is to increase the utilization of robots through the development of a whole body control algorithm for mobile cooperative robots and to improve work efficiency when operating in the workplace

* In addition, by implementing a simulator with a control algorithm, it is intended to be used to analyze risk factors between workers and robots and to review the work efficiency of mobile cooperative robots when developing workplace safety guidelines for mobile cooperative robots.

***    

#### <i class="far fa-edit"></i>  **Project Contents**   

**_Development of Mechanical Models for Mobile Cooperative Robots_**    
- Conducting mechanical modeling of the mobile cooperative provided robots 
- Verification of results of mechanical modeling through simulation    
   
*When developing a mechanical model, an integrated mechanical model was developed based on instrumental information of cooperative robots and mobile robots (6 degrees of freedom cooperative robots, 3 degrees of freedom mobile robots).*    
*Additional mathematical modeling was included when Jacobian or inverse mechanical analysis was required in the development of the Whole Body control algorithm*


**_Development of Wholebody Control Algorithm for Mobile Cooperative Robots_**
- Development of a location-based Whole Body control algorithm model.
- Deriving Control Inputs for Whole Body Control of Mobile and Cooperative Robots.
- Development of a Foldbody Control Algorithm Considering Singularity in the Work Area.



**_Implementation of a Mobile Cooperative Robot Simulator with Wholebody Control Algorithm_**
* Apply the wholebody control algorithm of mobile cooperative robot to the simulator provided (Simulator provided after contract)
* Development of 2 examples of applying the wholebody control algorithm

{% capture col1 %}
{%
  include figure.html
  image="images/project/dgist_project_2.png"
  caption="Ex1 ) Following sine wave"
%}
{% endcapture %}
{% capture col2 %}
{%
  include figure.html
  image="images/project/dgist_project_3.png"
  caption = "Ex2 ) Keeping the distal end at the same point"
%}
{% endcapture %}
{% include two-col.html col1=col1 col2=col2 %}    



***    
#### **<i class="fas fa-user-circle"></i> Participating Researchers**
* [**Wansoo Kim**](http://harco.hanyang.ac.kr/members/Wansoo-Kim.html)   : **_Principal Investigator_**  
* [**Inhyuk Baek**](http://harco.hanyang.ac.kr/members/Inhyuk-Baek.html)   : *(S/W) Project Manager ,  Control Algorithm Development*
* [**Seungmin Choi**](http://harco.hanyang.ac.kr/members/Seungmin-Choi.html)   : *(S/W) Control Algorithm Development*




***

#### **<i class="fas fa-money-bill-wave-alt"></i> Funding**

{%
  include feature.html
  image="images/project/dgist_support.png"
  link='https://www.dgist.ac.kr/kr/'
%}   
***   