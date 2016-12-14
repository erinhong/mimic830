import random
import csv

def count(fileName):
  numRows = 0
  with open(fileName, 'rU') as f:
    reader = csv.reader(f,delimiter = ",")
    data = list(reader)
    row_count = len(data)-1
  return row_count



def induceGaps(percentage_to_delete, total_rows, col_to_delete):
  with open("dead_ace_test.csv", 'rU') as f:
    reader = csv.DictReader(f,delimiter = ",")
    headers = reader.fieldnames
    headers.append('removed')
    print headers

    fileName = 'induced_dead_ace_test_'+str(percentage_to_delete)+'.csv'
    with open(fileName, 'w') as nf:
      writer = csv.DictWriter(nf, headers)

      num_to_delete = (int) (total_rows * percentage_to_delete)
      rows_to_delete = set(random.sample(range(1, total_rows), num_to_delete))

      c = 1
      writer.writeheader()
      for line in reader:
        if c in rows_to_delete:
          line['removed'] = line[col_to_delete]
          line[col_to_delete] = ""
        writer.writerow(line)
        c += 1




if __name__=='__main__':
  gradient = [.1,.3,.5]
  total_count = count("dead_ace_test.csv")


  for g in gradient: 
    induceGaps(g, total_count, "resprate")
