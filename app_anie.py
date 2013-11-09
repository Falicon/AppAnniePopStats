# -*- coding: utf-8 -*-

import cookielib
import mechanize
import re

def pull_html(url):
  br = mechanize.Browser()
  cj = cookielib.LWPCookieJar()
  br.set_cookiejar(cj)
  br.set_handle_robots(False)
  br.addheaders = [('User-agent', 'csv bot v0.01')]
  r = br.open(url)
  data = r.read()
  data = re.sub(r'\n', ' ', data)
  return data

types = {
  'iphone_free':[],
  'iphone_paid':[],
  'iphone_grossing':[],
  'android_free':[],
  'android_paid':[],
  'android_grossing':[],
  'android_top_new_free':[],
  'android_top_new_paid':[]
}
data = pull_html('http://www.appannie.com/apps/ios/top/?device=iphone')
items = data.split('<tr')
for item in items:
  cols = item.split('main-info')
  slot = 0
  for col in cols:
    m = re.search(r'^"><span title="([^"]+)"', col)
    if m:
      name = m.group(1).strip()
      if slot == 0:
        types['iphone_free'].append(name)
      if slot == 1:
        types['iphone_paid'].append(name)
      if slot == 2:
        types['iphone_grossing'].append(name)
      slot += 1

data = pull_html('http://www.appannie.com/apps/google-play/top/united-states')
items = data.split('<tr')
for item in items:
  cols = item.split('main-info')
  slot = 0
  for col in cols:
    m = re.search(r'^"><span title="([^"]+)"', col)
    if m:
      name = m.group(1).strip()
      if slot == 0:
        types['android_free'].append(name)
      if slot == 1:
        types['android_paid'].append(name)
      if slot == 2:
        types['android_grossing'].append(name)
      if slot == 3:
        types['android_top_new_free'].append(name)
      if slot == 4:
        types['android_top_new_paid'].append(name)
      slot += 1

# now just need to create csv
lines = []
for key in types.keys():
  line_count = 0
  if len(lines) - 1 > 0:
    lines[0].append('"%s"' % key)
  else:
    lines.append(['0', '"%s"' % key])
  for item in types[key]:
    line_count += 1
    try:
      # already have this line; just append to it
      lines[line_count].append('"%s"' % item)
    except:
      # don't have this line so need to set it up
      lines.append(['%s' % line_count, '"%s"' % item])

f = open('app_sales_data.csv', 'w')
for line in lines:
  f.write(', '.join(line))
  f.write('\n')
  
