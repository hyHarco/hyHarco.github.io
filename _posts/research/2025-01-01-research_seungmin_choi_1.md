---
title: Stable Variable Impedance Control via CLF-MPC for Physical Human-Robot Interaction 
image: images/research/seungmin_main.png
tags:
  - Compliance control
  - pHRC,pHRI
  - Model predictive control
  - Stability
author: Seungmin-Choi
member: Seungmin-Choi
group: research_2
---
**Goal** : Predicting impedance parameters to ensure the stability of variable impedance control via CLF-MPC
***

**Summary**
Variable impedance control is a control strategy widely used in physical human-robot collaboration (pHRC) and physical human-robot interaction (pHRI). Variable stiffness and damping parameters improve adaptability to changing environments and enhance safety in human-robot interaction. However, these adaptive parameters can compromise the stability of the system without proper management, particularly in dynamic environments. 
To address this, we propose a real-time parameter prediction method for variable impedance control using model predictive control (MPC) with Control Lyapunov Function (CLF). Unlike the method that sets the terminal constraint as the equilibrium position, the proposed method guarantees system stability even when parameters change or external disturbances occur, ensuring safe and adaptive robot behavior. Moreover, the infeasibility issue is resolved by applying CLF instead of relying on the equilibrium position. Furthermore, considering stability throughout the prediction horizon, the stability of the system is strictly guaranteed.    

***

<!-- **Topic**    
 * Compliance control
 * pHRC,pHRI
 * Model predictive control 
 * Stability -->


***


{%
  include figure.html
  image="images/research/seungmin_main.png"
%}


{% capture col1 %}

{%
  include figure.html
  image="images/research/seungmin_1.png"
%}
{% endcapture %}
{% capture col2 %}
{%
  include figure.html
  image="images/research/seungmin_2.png"
%}
{% endcapture %}
{% include two-col.html col1=col1 col2=col2 %}