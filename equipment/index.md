---
title: equipment
nav:
  order: 4
---

# **Robots & Equipment**

Hardware platforms and instrumentation supporting our research in human-robot collaboration, exoskeletons, and embodied AI.

<style>
  .eq_grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 24px;
    margin: 16px 0 8px;
  }
  .eq_item {
    display: flex;
    flex-direction: column;
  }
  .eq_thumb {
    width: 100%;
    aspect-ratio: 1 / 1;
    background: #ffffff;
    border: 1px solid #d6d6d4;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .eq_thumb img {
    max-width: 88%;
    max-height: 88%;
    width: auto;
    height: auto;
    object-fit: contain;
  }
  .eq_caption {
    margin-top: 12px;
    font-size: 0.92rem;
    line-height: 1.4;
  }
  .eq_caption b { color: #1d1d1b; }
  .eq_caption a { font-size: 0.78rem; color: #1f3b6e; }
  .eq_caption .eq_links { display: block; margin-top: 4px; color: #4a4a48; }

  @media (max-width: 900px) {
    .eq_grid { grid-template-columns: repeat(3, 1fr); }
  }
  @media (max-width: 640px) {
    .eq_grid { grid-template-columns: repeat(2, 1fr); }
  }
</style>

{% include section.html %}

<h3><i class="fa fa-caret-right" aria-hidden="true"></i> <b>Robot Platforms</b></h3>

<div class="eq_grid">
  <div class="eq_item">
    <div class="eq_thumb"><img src="/images/equipment/moca.png" loading="lazy" alt="MOCA"/></div>
    <div class="eq_caption"><b>MOCA Mobile Manipulator</b>
      <span class="eq_links"><a href="https://franka.de/">Franka Panda</a> · <a href="https://robotnik.eu/">Robot Nik</a> · <a href="https://qbrobotics.com/">qb robotics</a></span>
    </div>
  </div>
  <div class="eq_item">
    <div class="eq_thumb"><img src="/images/equipment/neuromek.png" loading="lazy" alt="NeuroMeka Moby"/></div>
    <div class="eq_caption"><b>NeuroMeka Moby</b>
      <span class="eq_links"><a href="https://www.neuromeka.com/">NeuroMeka</a></span>
    </div>
  </div>
  <div class="eq_item">
    <div class="eq_thumb"><img src="/images/equipment/piper.png" loading="lazy" alt="PiPER"/></div>
    <div class="eq_caption"><b>PiPER Robotic Arm</b>
      <span class="eq_links"><a href="https://global.agilex.ai/">AGILE X</a></span>
    </div>
  </div>
  <div class="eq_item">
    <div class="eq_thumb"><img src="/images/equipment/go2.png" loading="lazy" alt="Go2"/></div>
    <div class="eq_caption"><b>Go2</b>
      <span class="eq_links"><a href="https://www.unitree.com/go2">UNITREE</a></span>
    </div>
  </div>
</div>

{% include section.html %}

<h3><i class="fa fa-caret-right" aria-hidden="true"></i> <b>Motion Capture & Analysis</b></h3>

<div class="eq_grid">
  <div class="eq_item">
    <div class="eq_thumb"><img src="/images/equipment/xsens_motioncapture.png" loading="lazy" alt="Xsens MTW"/></div>
    <div class="eq_caption"><b>Xsens MTW Motion Capture</b>
      <span class="eq_links"><a href="https://www.movella.com/">Movella</a></span>
    </div>
  </div>
  <div class="eq_item">
    <div class="eq_thumb"><img src="/images/equipment/optitrack_motioncapture.png" loading="lazy" alt="Optitrack"/></div>
    <div class="eq_caption"><b>Optitrack Motion Capture</b>
      <span class="eq_links"><a href="https://optitrack.com/">Optitrack</a></span>
    </div>
  </div>
  <div class="eq_item">
    <div class="eq_thumb"><img src="/images/equipment/perneuron_motioncapture.png" loading="lazy" alt="Perception Neuron"/></div>
    <div class="eq_caption"><b>Perception Neuron Motion Capture</b>
      <span class="eq_links"><a href="https://neuronmocap.com/">Perception Neuron</a></span>
    </div>
  </div>
  <div class="eq_item">
    <div class="eq_thumb"><img src="/images/equipment/anybody.png" loading="lazy" alt="AnyBody"/></div>
    <div class="eq_caption"><b>AnyBody Motion Analysis</b>
      <span class="eq_links"><a href="https://www.anybodytech.com/">AnyBody Technology</a></span>
    </div>
  </div>
</div>

{% include section.html %}

<h3><i class="fa fa-caret-right" aria-hidden="true"></i> <b>AR/VR & Sensors</b></h3>

<div class="eq_grid">
  <div class="eq_item">
    <div class="eq_thumb"><img src="/images/equipment/metaquest.png" loading="lazy" alt="MetaQuest"/></div>
    <div class="eq_caption"><b>MetaQuest VR System</b>
      <span class="eq_links"><a href="https://www.metaquest.co.kr/">MetaQuest</a></span>
    </div>
  </div>
  <div class="eq_item">
    <div class="eq_thumb"><img src="/images/equipment/hololens.png" loading="lazy" alt="HoloLens"/></div>
    <div class="eq_caption"><b>HoloLens AR System</b>
      <span class="eq_links"><a href="https://www.microsoft.com/en-us/hololens">Microsoft</a></span>
    </div>
  </div>
  <div class="eq_item">
    <div class="eq_thumb"><img src="/images/equipment/delsysemg.png" loading="lazy" alt="Delsys EMG"/></div>
    <div class="eq_caption"><b>Delsys EMG System</b>
      <span class="eq_links"><a href="https://delsys.com/trigno-emg/">Delsys</a></span>
    </div>
  </div>
  <div class="eq_item">
    <div class="eq_thumb"><img src="/images/equipment/amtiforceplate.png" loading="lazy" alt="AMTI Force Plate"/></div>
    <div class="eq_caption"><b>AMTI Force Plate</b>
      <span class="eq_links"><a href="https://amti.biz/">AMTI</a></span>
    </div>
  </div>
</div>
