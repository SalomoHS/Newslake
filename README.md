<p align="center">
  <h3 align="center">Newslake</h3>
</p>

<p align="center">
  <a href="https://git.io/typing-svg"><img src="https://readme-typing-svg.demolab.com?font=Fira+Code&pause=1000&color=175D9C&center=true&vCenter=true&width=435&lines=Collect%2C+explore%2C+and+stay+updated" alt="Typing SVG" /></a>
</p>

<p align="center">
  Couriousity drive me to developed this tools <br> Make me easier for view latest news without visiting multiple news portal. 
</p>

<p align="center">
    <img alt="Python" title="Python" src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54"/>
</p>

<p align="center">
    <img alt="Pandas" title="Pandas" src="https://img.shields.io/badge/Pandas-150458?logo=pandas&logoColor=fff"/>
    <img alt="Matplotlib" title="Matplotlib" src="https://custom-icon-badges.demolab.com/badge/Matplotlib-71D291?logo=matplotlib&logoColor=fff"/>
    <img alt="Google Translate" title="Google Translate" src="https://img.shields.io/badge/Google%20Translate-%234285F4.svg?logo=googletranslate&logoColor=white"/>
   <img alt="Scikit Learn" title="Scikit Learn" src="https://img.shields.io/badge/Scikit%20Learn-F38020?logo=scikitlearn&logoColor=white"/>
  <img alt="BeautifulSoup" title="BeautifulSoup" src="https://img.shields.io/badge/BeautifulSoup-57A143?logo=package-24&logoColor=white"/>
</p>

---

### Usage
- Get news
```python
import newslake
nl = newslake.get_news(regions=['id'],topics=["international"],n_news=5,language='id') # Return pandas dataframe
nl.head(5) 
```
- Generate wordcloud
```python
nl.wordcloud()
```
- Generate Timeseries Wordcloud
```python
nl.timeseries_wordcloud()
```

---

### Program Flow
1. User given parameter through `get_news` attribute
2. Request to each news portal RSS based on inputed parameter
3. Parse the RSS to get attribute (article link, title, published date, content) using BeautifulSoup
4. Translate content based on `language` parameter using google translate
5. Convert data to pandas dataframe
   
---

### The Author
<img alt="Salomo Hendrian Sudjono" title="Salomo Hendrian Sudjono" src="https://custom-icon-badges.demolab.com/badge/-Salomo%20Hendrian%20Sudjono-blue?style=for-the-badge&logo=person-fill&logoColor=white"/>
