**ColNet**

Creating collaboration network from scratch, including crawling from Google Scholar and Microsoft Academic Search, visualization with Basemap

![collaboration network](https://github.com/horsehour/colnet/raw/master/academicit2.png)


**Step 1**:  **Crawling list of publications from Google Scholar Profile pages, or Preview version of Microsoft Academic**

Google Scholar Profile: https://scholar.google.com/citations?user=[pid]&hl=en

Microsoft Academic: https://preview.academic.microsoft.com/api/entity/[pid]?entityType=2

Each [pid] in the above urls corresponds to one scholar. Google and Microsoft have their own approach to define the IDs. The problems are that some scholars may do not have an ID, or the same person have more than one IDs due to job transfering from one affiliation to another one, or they have more than one positions in different affiliations. To our case, these difference are completely ignored.

- see **zhizhuprofilema.py**, **zhizhuma.py** 

**Step 2: Extracting coauthors from publication/paper page**

Problems we are facing include: (1) authors' names may have varied forms in different publications (2) one name may be related to different person.

The first problem cause another issue, their ids may be different since the search engines fails to recognize these names as the the same person, theirfore different names of one person could have multiple profile pages. We do not make further investigation, just considering the IDs.

The extracted authors, specifically the authors and their IDs assigned by search engines are saved and from which we build up the coauthorship. 

- see **zhizhupprofilema.py**, **profiles.py**  

**Step 3: Visualization of the coauthorship in collaboration network**

There are several ways to visualize the collaboration network based on whether their geolocations are considered. If geolocations are not considered, it's very simple, and there are untold numbers of tools can deal with it. However, when geolocations are considered, we have to face the fact that we need to crawl geolocation for each affiliation.

The affiliations are collected when extract the profiles of authors, and most of our data are collected from Microsoft Academic, because Google scholar does not provide sufficient information of authors, where lots of scholars' affiliations are missed. 

— **Extract affiliations from the author profile page**

— **Collect geolocation information**

To collect geolocation information (longitude and latitude data) of affiliationns, we apply a Google map API. It provides the searching service that gives us the geolocation of a place, either an address or the name of a company or an affiliation. Though the service is not perfect, some places can not located in Google map, it helps to save majority of our manual operations. With the geolocations of several missed affiliations filled, we build up the mapping from an affiliation to its geolocations. 

- see **geocode.py**

We visualize these affiliations on a map, and wire the coauthorship between authors, which gives the spatial collaboration network. The visualization tool we are using is [mpl_toolkits.basemap](https://matplotlib.org/basemap/users/installing.html).

- see **summary.py**,**visualize_citnet.py**