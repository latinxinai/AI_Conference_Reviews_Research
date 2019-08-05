import pandas as pd
import csv
import time
import concurrent.futures
from openreview import openreview


def save_venue_to_csv(client, venue, csv_filename):
  """Given the url of a venue retrieves the data to a csv file

  Args:
    client (Client object from openreview): Specifies the base URL
      and the login infomation
    venue (string): Each string is a URL to a conference
    csv_filename (string): Name or path for the resulting csv file 
  Yields:
    A csv file name as csv_filename.csv that contains review data.
  """
  submitted_papers = list(openreview.tools.iterget_notes(client, invitation=venue))

  with open(csv_filename+".csv", 'w') as csv_file:
    csv_file.write("title,authors,emails,decision,abstract,pdf,replies\n") # header
    for paper in submitted_papers:
      tmp = paper.to_json()
      forum_id = tmp['forum']
      decision = ""
      content_keys = tmp["content"].keys()
      if 'decision' in content_keys:
        decision = tmp['content']['decision']
      elif 'recommendation' in content_keys:
        decision = tmp['content']['recommendation']
      forum_comments = client.get_notes(forum=str(forum_id))
      writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
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
  csv_file.close()

def retrieve_data_from_paper(client, paper):
  """Given the url of a venue retrieves the data to a csv file

  Args:
	 	client (Client object from openreview): Specifies the base URL
      and the login infomation
		paper (string): Piece of text that identifies the paper in the venue
    
  Returns:
    A list of strings corresponding to the data fetched from a peper id,
    the list represents a row for the csv file in the following order:
    
    title,authors,emails,decision,abstract,pdf,replies

    Where replies contains in all the replies for the paper as a string
    with list format for example:
    
    [[('title', 'review of Deep Learning'), 
    ('review', "This paper ... )')], 
    [('title', 'review of Deep Learning')]]

	"""

  tmp = paper.to_json()
  forum_id = tmp['forum']
  content_keys = tmp["content"].keys()
  decision = ""
  if 'decision' in content_keys:
    decision = tmp['content']['decision']
  elif 'recommendation' in content_keys:
    decision = tmp['content']['recommendation']
  forum_comments = client.get_notes(forum=str(forum_id))
  
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
  
  return row

def save_venue_to_csv_parallel(client, venue, csv_filename, n_workers=8):
  '''Given the url of a venue retrieves the data to a csv file

  Args:
    client (Client object from openreview): Specifies the base URL
      and the login infomation
    venue (string): Each string is a URL to a conference
    csv_filename (string): Name or path for the resulting csv file 
    n_workers (optional int): It specifies the number of workers
	Yields:
    A csv file name as csv_filename.csv that contains review data.
  '''
  submitted_papers = list(openreview.tools.iterget_notes(client, invitation=venue))

  results = []
  with concurrent.futures.ThreadPoolExecutor(max_workers=n_workers) as executor:
    futures = []
    for paper in submitted_papers:
      futures.append(executor.submit(retrieve_data_from_paper, client, paper))
    for future in concurrent.futures.as_completed(futures):
      results.append(future.result())
  
  with open(csv_filename+".csv", 'w') as csv_file:
    csv_file.write("title,authors,emails,decision,abstract,pdf,replies\n") # header
    writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
    for row in results:
      writer.writerow(row)
  csv_file.close()

def save_all_venues_to_csv(client, venues, csv_filenames, n_workers=8, parallel=True):
  '''Given a the list of urls of the venues retrieves all the review data into csv files

  Args:
    client (Client object from openreview): Specifies the base URL
      and the login infomation
    venues (list of strings): Each string is a URL to a conference
    csv_filename (list of strings): Name or path for the resulting csv file 
    n_workers (optional int): It specifies the number of workers
		parallel (bool): To do this parallel using n_workers
  Yields:
    Csv files that contains review data.
	'''

  if parallel:
    for i in range(len(venues)):
      save_venue_to_csv_parallel(client, venues[i], csv_filenames[i], n_workers)
      print("Venue "+str(i)+" done.")
  else:
    for i in range(len(venues)):
      save_venue_to_csv_parallel(client, venues[i], csv_filenames[i])
      print("Venue "+str(i)+" done.")

def main():

  path_to_data = "iclr_urls.csv"
  iclr_conf_data = pd.read_csv(path_to_data) 
  iclr_conf_data.head()

  start = time.time()

  # Using guest mode
  client = openreview.Client(baseurl='https://openreview.net')

  url_list = list(iclr_conf_data["conference_url"])
  conference_list = list(iclr_conf_data["conference"])

  save_all_venues_to_csv(client, url_list, conference_list, 8)

  end = time.time()
  print(end - start)

if __name__ == "__main__":
    main()