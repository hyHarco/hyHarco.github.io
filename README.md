# Harco LAB

## Testing Webpage site locally with Jekyll

### Prerequisites
Before you can use Jekyll to test a site, you must:
* Intall [jekyll](https://jekyllrb.com/docs/installation/)
* Create a Jekyll site, see more [HERE](https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll/creating-a-github-pages-site-with-jekyll)

We recommend using [Bundler](http://bundler.io/) to install and run Jekyll. Bundler manages Ruby gem dependencies, reduces Jekyll build errors, and prevents environment-related bugs. To install Bundler:

### Building the site locally
1. Open Terminal.
2. Navigate to local repo source for your site.
```bash
$ cd hyHarco.github.io
```
3. Run the Jekyll site locally.
```bash
$ bundle exec jekyll serve
```
4. To preview the site, in your web browser, navigate to ```http://localhost:4000```.