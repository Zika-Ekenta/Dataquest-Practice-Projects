#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().run_cell_magic('capture', '', '%load_ext sql\n%sql sqlite:///factbook.db')


# In[2]:


get_ipython().run_cell_magic('sql', '', "SELECT *\n  FROM sqlite_master\n WHERE type='table';")


# In[3]:


get_ipython().run_cell_magic('sql', '', 'SELECT *\n    FROM facts\n    LIMIT 5')


# In[4]:


get_ipython().run_cell_magic('sql', '', 'SELECT MIN(population) as min_pop,\n       MAX(population) as max_pop, MIN(population_growth) as min_growth,MAX(population_growth) as max_growth\n    from facts\n    ')


# A few obvious things to highight: there is a country with zero population and a country with over 7 billion people. We need to investigate why this is so. We'll start with the minimum population.

# In[5]:


get_ipython().run_cell_magic('sql', '', 'select *\n    FROM facts\n    WHERE population = (SELECT MIN (population)\n                           FROM facts)\n    \n    ')


# This actually makes a bit of sense since Antartica isn't know to have an indigenous human presence.

# In[6]:


get_ipython().run_cell_magic('sql', '', 'select *\n    FROM facts\n    WHERE population = (SELECT MAX (population)\n                           FROM facts)\n    ')


# This seems to be an estimate of the total world population.

# In[7]:


get_ipython().run_cell_magic('sql', '', "SELECT MIN(population) as min_pop,MAX(population) as max_pop, MIN(population_growth) as min_growth,MAX(population_growth) as max_growth\n    from facts\n    where name != 'World'")


# It appears the new max population is 1.36bn. I suspect this is China.

# In[8]:


get_ipython().run_cell_magic('sql', '', "select AVG(population), AVG(area)\n    from facts\n    where name != 'World'")


# Let's have a look at the most densely populated countries on earth. Our approach will be countrie where population is higher than average AND area is less than average.

# In[19]:


get_ipython().run_cell_magic('sql', '', "SELECT name, population, area, (CAST(population AS FLOAT)/area) AS pop_density\n    FROM facts\n    WHERE population >(SELECT AVG(population)\n                         FROM facts\n                         WHERE name != 'World' )  \n    AND area < (SELECT AVG(area)\n                  FROM facts\n                  WHERE name != 'World')\n    ORDER BY pop_density Desc")


# Some of these countries are known to be densely populated, so we're looking good. However, i expected to see Nigeria in this list.

# Out of curiousity i want to know the countries with the largest water to land ratios, so i can plan my next holiday.

# In[18]:


get_ipython().run_cell_magic('sql', '', "SELECT name, (CAST(area_water AS FLOAT) /area_land ) AS water_land_ratio\n    FROM FACTS\n    WHERE name != 'World'\n    ORDER BY water_land_ratio DESC;")

