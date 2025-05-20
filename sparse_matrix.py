class sparsematrix:
    def __init__(self, filepath=None, rows=0, cols=0):
        self.rows=rows
        self.cols=cols
        self.data={}


        if filepath:
            self.load_from_file(filepath)


    def load_from_file(self,filepath):
        try:
            with open(filepath,'r') as f:
                lines=f.readlines()

                newlines=[]

                for line in lines:
                    stripped = line.strip()
                    if stripped:
                        newlines.append(stripped)
                lines=newlines  

            if not lines[0].startswith('rows=') or not lines[1].startswith('cols='):
                raise ValueError('Input file has wrong format') 

            lineparts=lines[0].split('=')
            lineparts[1]= int(lineparts[1])
            self.rows = lineparts[1] 

            lineparts=lines[1].split('=')
            lineparts[1]= int(lineparts[1])
            self.cols=lineparts[1]

            for line in lines[2:]:
                if not(line.startswith('(') and  line.endswith(')')):
                    raise ValueError("Input file has wrong format")
                
                parts=line[1:-1].split(',')
                if len(parts) != 3:
                    raise ValueError('Input file has wrong format')
                
                r,c,v=parts[0].strip(), parts[1].strip(), parts[2].strip()

                if '.' in r or '.' in c or '.' in v:
                    raise ValueError('Input file has wrong format')
                
                r=int(parts[0])
                c=int(parts[1])
                v=int(parts[2])

                if v !=0:
                    if r not in self.data:
                        self.data[r]={}
                    self.data[r][c]=v
        
        
        except Exception as e:
            raise ValueError("Input file has wrong format") from e


    def getElement(self, row, col):
        return self.data.get(row, {}).get(col, 0)

    def setElement(self, row, col, value):
        if row >= self.rows or col >= self.cols:
            raise IndexError("Index out of bounds")

        if value == 0:
            if row in self.data and col in self.data[row]:
                del self.data[row][col]
                if not self.data[row]:
                    del self.data[row]
        else:
            if row not in self.data:
                self.data[row] = {}
            self.data[row][col] = value        
    


    def add_matrix(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrix dimensions do not match for addition")

        result = sparsematrix(rows=self.rows, cols=self.cols)
        all_rows = set(self.data.keys()) | set(other.data.keys())

        for r in all_rows:
            cols = set(self.data.get(r, {}).keys()) | set(other.data.get(r, {}).keys())
            for c in cols:
                val = self.getElement(r, c) + other.getElement(r, c)
                result.setElement(r, c, val)

        return result

    def subtract_matrix(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrix dimensions do not match for subtraction")

        result = sparsematrix(rows=self.rows, cols=self.cols)
        all_rows = set(self.data.keys()) | set(other.data.keys())

        for r in all_rows:
            cols = set(self.data.get(r, {}).keys()) | set(other.data.get(r, {}).keys())
            for c in cols:
                val = self.getElement(r, c) - other.getElement(r, c)
                result.setElement(r, c, val)

        return result

    def multiply_matrix(self, other):
        if self.cols != other.rows:
            raise ValueError("Matrix dimensions do not match for multiplication")

        result = sparsematrix(rows=self.rows, cols=other.cols)

        for r in self.data:
            for c1 in self.data[r]:
                if c1 in other.data:
                    for c2 in other.data[c1]:
                        prev = result.getElement(r, c2)
                        result.setElement(r, c2, prev + self.data[r][c1] * other.data[c1][c2])

        return result
    

    def resultsFile(self, file_path):
        with open(file_path, 'w') as f:
            f.write(f"rows={self.rows}\n")
            f.write(f"cols={self.cols}\n")
            for r in sorted(self.data):
                for c in sorted(self.data[r]):
                    v = self.data[r][c]
                    f.write(f"({r}, {c}, {v})\n")

def main():
     print("Please choose the operation of your choice:\n1. Addition\n2. Subtraction\n3. Multiplication")
     operation = input("Enter your choice (1/2/3): ").strip()

     file1 = input("Enter path to first matrix file: ").strip()
     file2 = input("Enter path to second matrix file: ").strip()

     try:
        m1 = sparsematrix(file1)
        m2 = sparsematrix(file2)

        if operation == '1':
            result = m1.add_matrix(m2)
            result_file = "result_add.txt"
        elif operation == '2':
            result = m1.subtract_matrix(m2)
            result_file = "result_subtract.txt"
        elif operation == '3':
            result = m1.multiply_matrix(m2)
            result_file = "result_multiply.txt"
        else:
            print("Invalid operation selected.")
            return

        result.resultsFile(result_file)
        print(f"Operation successful! Result written to {result_file}")

     except Exception as e:
        print("Error:", e)

if __name__ == "__main__":  
    main()    