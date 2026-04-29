---
title: Home
layout: default
---

<!-- Swiper CSS -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swiper@10/swiper-bundle.min.css" />

<style>
  .home_hero {
    margin: 0 0 48px;
  }
  .home_hero .mySwiper {
    width: 100%;
    aspect-ratio: 21 / 9;
    max-height: 60vh;
    min-height: 280px;
    overflow: hidden;
    border: none;
    background: #ffffff;
  }
  .home_hero .mySwiper .swiper-slide {
    display: flex;
    align-items: center;
    justify-content: center;
    background: #ffffff;
  }
  .home_hero .mySwiper .swiper-slide img {
    width: auto;
    height: auto;
    max-width: 100%;
    max-height: 100%;
    object-fit: contain;
    display: block;
  }
  .home_hero .mySwiper .swiper-slide.cover img {
    width: 100%;
    height: 100%;
    max-width: none;
    max-height: none;
    object-fit: cover;
  }
  .home_hero .swiper-button-next,
  .home_hero .swiper-button-prev { color: #ffffff; }
  .home_hero .swiper-pagination-bullet-active { background: #ffffff; }

  .home_eyebrow {
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #1f3b6e;
    margin: 0 0 12px;
  }
  .home_intro {
    display: grid;
    grid-template-columns: 240px 1fr;
    gap: 56px;
    align-items: center;
    margin: 0 0 40px;
  }
  .home_intro_logo {
    display: flex;
    justify-content: center;
  }
  .home_intro_logo img {
    width: 100%;
    max-width: 240px;
    height: auto;
    display: block;
  }
  .home_intro_text > *:first-child {
    margin-top: 0;
  }
  @media (max-width: 800px) {
    .home_intro {
      grid-template-columns: 1fr;
      gap: 24px;
      align-items: start;
    }
    .home_intro_logo { justify-content: flex-start; }
    .home_intro_logo img { max-width: 200px; }
  }

  .home_title {
    font-family: "Inter", sans-serif;
    font-size: 1.6rem;
    font-weight: 600;
    letter-spacing: -0.01em;
    line-height: 1.25;
    margin: 0 0 20px;
    color: #1d1d1b;
  }
  .home_lead {
    font-size: 1.05rem;
    line-height: 1.7;
    color: #4a4a48;
    margin: 0 0 18px;
  }
  .home_lead b { color: #1d1d1b; }
  .home_cta {
    margin-top: 28px;
    padding: 18px 22px;
    border-left: 3px solid #1f3b6e;
    background: #f5f5f3;
    font-size: 0.95rem;
    color: #1d1d1b;
  }
  .home_cta a { color: #1f3b6e; font-weight: 600; }

  /* Research Topics */
  .home_topics {
    margin: 16px 0 8px;
    padding: 32px 40px 24px;
  }
  .home_topics_head {
    margin: 0 0 28px;
  }
  .home_topics_head h2 {
    font-family: "Inter", sans-serif;
    font-size: 1.25rem;
    font-weight: 600;
    letter-spacing: -0.01em;
    margin: 0;
    padding: 0;
    border: none;
    color: #1d1d1b;
  }
  .home_topics_grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 24px;
  }
  .topic_card {
    position: relative;
    display: flex;
    flex-direction: column;
    background: #ffffff;
    color: #1d1d1b;
    text-decoration: none;
    padding: 0 0 18px;
    border: 1px solid #d6d6d4;
    transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
  }
  .topic_card:hover {
    border-color: #1f3b6e;
    transform: translateY(-3px);
    box-shadow: 0 10px 24px rgba(17, 35, 73, 0.08);
  }
  .topic_card:hover .topic_card_image img { transform: scale(1.04); }
  .topic_card_image {
    position: relative;
    width: 100%;
    margin: 0 0 16px;
    aspect-ratio: 16 / 10;
    overflow: hidden;
    background: #f7f9fc;
  }
  .topic_card_image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
    transition: transform 0.3s ease;
  }
  .topic_card_body {
    padding: 0 18px;
  }
  .topic_card_title {
    font-family: "Inter", sans-serif;
    font-size: 1.1rem;
    font-weight: 600;
    letter-spacing: -0.005em;
    margin: 0 0 10px;
    color: #1d1d1b;
  }
  .topic_card_more {
    font-family: "Inter", sans-serif;
    font-size: 0.85rem;
    font-weight: 500;
    color: #1f3b6e;
    letter-spacing: 0.02em;
  }

  @media (max-width: 800px) {
    .home_topics_grid { grid-template-columns: 1fr; gap: 18px; }
  }

  /* News strip */
  .home_news {
    margin: 64px 0 16px;
    padding: 32px 40px 24px;
    border-top: 1px solid #d6d6d4;
  }
  .home_news_head {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin: 0 0 16px;
    gap: 16px;
    flex-wrap: wrap;
  }
  .home_news_head h2 {
    font-family: "Inter", sans-serif;
    font-size: 1.25rem;
    font-weight: 600;
    letter-spacing: -0.01em;
    margin: 0;
    padding: 0;
    border: none;
    color: #1d1d1b;
  }
  .home_news_more {
    font-size: 0.85rem;
    color: #1f3b6e;
    text-decoration: none;
    font-weight: 500;
  }
  .home_news_more:hover { color: #112349; }
  .home_news_list {
    list-style: none;
    padding: 0;
    margin: 0;
    border-top: 1px solid #ececea;
  }
  .home_news_list li {
    border-bottom: 1px solid #ececea;
  }
  .home_news_list a {
    display: grid;
    grid-template-columns: 110px 1fr;
    align-items: baseline;
    gap: 18px;
    padding: 8px 0;
    color: #1d1d1b;
    text-decoration: none;
    transition: color 0.15s ease;
  }
  .home_news_list a:hover { color: #1f3b6e; }
  .home_news_list time {
    font-family: "Inter", sans-serif;
    font-size: 0.85rem;
    font-weight: 500;
    letter-spacing: 0;
    color: #4a4a48;
    white-space: nowrap;
  }
  .home_news_list .home_news_title {
    font-size: 0.98rem;
    line-height: 1.4;
  }

  /* YouTube strip */
  .home_youtube {
    margin: 16px 0 8px;
    padding: 32px 40px 24px;
  }
  .home_youtube_head {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin: 0 0 16px;
    gap: 16px;
    flex-wrap: wrap;
  }
  .home_youtube_head h2 {
    font-family: "Inter", sans-serif;
    font-size: 1.25rem;
    font-weight: 600;
    letter-spacing: -0.01em;
    margin: 0;
    padding: 0;
    border: none;
    color: #1d1d1b;
  }
  .home_youtube_more {
    font-size: 0.85rem;
    color: #1f3b6e;
    text-decoration: none;
    font-weight: 500;
  }
  .home_youtube_more:hover { color: #112349; }
  .home_youtube_grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 22px;
    max-width: 880px;
  }
  .home_youtube_card {
    display: flex;
    flex-direction: column;
    text-decoration: none;
    color: #1d1d1b;
    transition: color 0.15s ease, transform 0.2s ease;
  }
  .home_youtube_card:hover {
    color: #1f3b6e;
    transform: translateY(-2px);
  }
  .home_youtube_card:hover .home_youtube_play { opacity: 1; }
  .home_youtube_card:hover .home_youtube_thumb img { transform: scale(1.04); }
  .home_youtube_thumb {
    position: relative;
    width: 100%;
    aspect-ratio: 16 / 9;
    overflow: hidden;
    background: #f5f5f3;
    border: 1px solid #d6d6d4;
  }
  .home_youtube_thumb img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
    transition: transform 0.3s ease;
  }
  .home_youtube_play {
    position: absolute;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #ffffff;
    font-size: 1.6rem;
    background: rgba(0, 0, 0, 0.32);
    opacity: 0.85;
    transition: opacity 0.2s ease;
    pointer-events: none;
  }
  .home_youtube_meta {
    display: flex;
    flex-direction: column;
    gap: 4px;
    padding: 10px 0 0;
  }
  .home_youtube_meta time {
    font-family: "Inter", sans-serif;
    font-size: 0.78rem;
    font-weight: 500;
    letter-spacing: 0;
    color: #4a4a48;
  }
  .home_youtube_title {
    font-size: 0.92rem;
    line-height: 1.35;
    color: #1d1d1b;
    text-decoration: none;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
    transition: color 0.15s ease;
  }
  .home_youtube_title:hover {
    color: #1f3b6e;
  }

  @media (max-width: 900px) {
    .home_youtube_grid { gap: 16px; max-width: 100%; }
  }
  @media (max-width: 700px) {
    .home_title { font-size: 1.55rem; }
    .home_news_list a { grid-template-columns: 92px 1fr; gap: 12px; }
    .home_news_list .home_news_title { font-size: 0.92rem; }
    .home_youtube { padding: 24px 20px 16px; }
    .home_youtube_grid { grid-template-columns: 1fr 1fr; gap: 12px; }
    .home_youtube_title { font-size: 0.85rem; }
  }
</style>

<section class="home_hero">
  <div class="swiper mySwiper">
    <div class="swiper-wrapper">
      <div class="swiper-slide"><img src="/images/main_img/1.png" alt="HARCO Lab"></div>
      <div class="swiper-slide cover"><img src="/images/main_img/2.png" alt="HARCO Lab"></div>
      <div class="swiper-slide"><img src="/images/main_img/3.png" alt="HARCO Lab"></div>
      <div class="swiper-slide"><img src="/images/main_img/4.png" alt="HARCO Lab"></div>
    </div>
    <div class="swiper-button-next"></div>
    <div class="swiper-button-prev"></div>
    <div class="swiper-pagination"></div>
  </div>
</section>

<div class="home_intro">
  <div class="home_intro_logo">
    <img src="/images/harc.png" alt="HARCO Lab" loading="lazy" />
  </div>

  <div class="home_intro_text">
    <h1 class="home_title">Hum<b>A</b>n-<b>R</b>obot <b>CO</b>llaboration Research Lab</h1>

    <p class="home_lead">
    We study how humans and robots can work together — physically, cognitively, and reliably. Our research spans Physical Human-Robot Interaction (pHRI), shared and whole-body control, ergonomics and human factors, haptic and tactile sensing, machine learning for robotics, and powered exoskeletons.
    </p>
  </div>
</div>

<div class="home_cta">Interested in joining the lab? Send your CV to <a href="mailto:wansookim+app@hanyang.ac.kr">wansookim+app@hanyang.ac.kr</a>.</div>

{% include home-topics-strip.html %}

{% include home-news-strip.html %}

{% include home-youtube-strip.html %}

<!-- Swiper JS -->
<script src="https://cdn.jsdelivr.net/npm/swiper@10/swiper-bundle.min.js"></script>
<script>
  const swiper = new Swiper(".mySwiper", {
    loop: true,
    autoplay: { delay: 5000, disableOnInteraction: false },
    pagination: { el: ".swiper-pagination", clickable: true },
    navigation: { nextEl: ".swiper-button-next", prevEl: ".swiper-button-prev" },
  });
</script>
