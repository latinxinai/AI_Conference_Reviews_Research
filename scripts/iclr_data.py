from openreview import openreview
from openreview import tools
import json
import csv
import pandas as pd
import requests

# ICLR

# 2013

iclr2013_conference = "ICLR.cc/2013/conference/-/submission" # 67

# 2014

iclr2014_conference = "ICLR.cc/2014/conference/-/submission" # 69
iclr2014_workshop = "ICLR.cc/2014/workshop/-/submission" # 19

# 2015 there was not ICLR on openreview

# 2016 just entries for workshop

iclr2016_workshop = "ICLR.cc/2016/workshop/-/submission" # 125

# 2017

iclr2017_conference = "ICLR.cc/2017/conference/-/paper.*/acceptance" # 490
iclr2017_workshop = "ICLR.cc/2017/workshop/-/paper.*/acceptance" # 124

# 2018

iclr2018_conference_decision = "ICLR.cc/2018/Conference/-/Acceptance_Decision" # 935
iclr2018_workshop_decision = "ICLR.cc/2018/Workshop/-/Acceptance_Decision" # 345

# 2019

iclr2019_conference_decision = "ICLR.cc/2019/Conference/-/Paper.*/Meta_Review" # 1419
iclr2019_workshop_drlmsp = "ICLR.cc/2019/Workshop/drlStructPred/-/Paper.*/Decision" # 8
iclr2019_workshop_rml = "ICLR.cc/2019/Workshop/RML/-/Paper.*/Decision" # 8
iclr2019_workshop_lld = "ICLR.cc/2019/Workshop/LLD/-/Paper.*/Decision" # 67
iclr2019_workshop_dgmhsd = "ICLR.cc/2019/Workshop/DeepGenStruct/-/Paper.*/Decision" # 42



venues = [iclr2013_conference,
          iclr2014_conference,
          iclr2014_workshop,
          iclr2016_workshop,
          iclr2017_conference,
          iclr2017_workshop,
          iclr2018_conference_decision,
          iclr2018_workshop_decision,
          iclr2019_conference_decision,
          iclr2019_workshop_drlmsp,
          iclr2019_workshop_rml,
          iclr2019_workshop_lld,
          iclr2019_workshop_dgmhsd]
      
venues_csv = ["iclr2013_conference",
              "iclr2014_conference",
              "iclr2014_workshop",
              "iclr2016_workshop",
              "iclr2017_conference",
              "iclr2017_workshop",
              "iclr2018_conference_decision",
              "iclr2018_workshop_decision",
              "iclr2019_conference_decision",
              "iclr2019_workshop_drlmsp",
              "iclr2019_workshop_rml",
              "iclr2019_workshop_lld",
              "iclr2019_workshop_dgmhsd"]


def save_venue_to_csv(client, venue, csv_filename):

  submitted_papers = list(openreview.tools.iterget_notes(client, invitation=venue))

  with open(csv_filename+".csv", 'w') as csvfile:
      csvfile.write("title,authors,authorids,decision,abstract,pdf,replies\n")
      for paper in submitted_papers:

          forum_id = paper.to_json()['forum']
          decision = ""
          content_keys = paper.to_json()["content"].keys()
          
          if 'decision' in content_keys:
            decision = paper.to_json()['content']['decision']
          elif 'recommendation' in content_keys:
            decision = paper.to_json()['content']['recommendation']
          forum_comments = client.get_notes(forum=str(forum_id))
          writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
          row = []
          replies = []
          for comment in forum_comments:
            if 'abstract' in comment.content.keys():
              row.append(comment.content["title"])
              row.append(comment.content['authors'])
              row.append(comment.content['authorids'])
              if 'decision' in comment.content.keys():
                row.append(comment.content['decision'])
              else:
                row.append(decision)
              row.append(comment.content["abstract"])
              row.append(comment.content["pdf"])
            else:
              replies.append(list(comment.content.items()))
          row.append(replies)
          writer.writerow(row)
  csvfile.close()

def save_all_venues_to_csv(client, venues, csv_filenames):
  
  for i in range(len(venues)):
    save_venue_to_csv(client, venues[i], csv_filenames[i])
    print("Venue "+str(i)+" done.")

def main():
  # Using guest mode
  client = openreview.Client(baseurl='https://openreview.net')

  # save_venue_to_csv(client, iclr2018_conference_withdrawn, 'iclr2018_conference_withdrawn')
  save_all_venues_to_csv(client, venues, venues_csv)


if __name__ == "__main__":
    main()
