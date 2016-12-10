import random
import csv

def count():
  numRows = 0
  with open("../ace.csv", 'r') as f:
    reader = csv.reader(f,delimiter = ",")
    data = list(reader)
    row_count = len(data)-1
  return row_count

def induceGaps(percentage_to_delete, total_rows, col_to_delete):
  with open("../ace.csv", 'r') as f:
    reader = csv.DictReader(f,delimiter = "\t")
    headers = reader.fieldnames
    with open("induced_ace.csv", 'a') as nf:
      writer = csv.DictWriter(nf, headers)

      num_to_delete = (int) (total_rows * percentage_to_delete)
      rows_to_delete = set(random.sample(range(1, total_rows), num_to_delete))

      count = 1
      for line in reader:
        if count in rows_to_delete:
          line[col_to_delete] = ""
        writer.writerow(line)
        count += 1

if __name__=='__main__':
  gradient = [.1,.3,.5]

  induceGaps(.1, count, "resprate")
