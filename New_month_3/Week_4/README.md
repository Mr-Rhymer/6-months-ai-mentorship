# Titanic Data Cleaning and Analysis

## Dataset
The Titanic passenger list from Kaggle (downloaded from [this link](https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv)).  
- **Rows:** 891 passengers  
- **Columns:** PassengerId, Survived (0 = died, 1 = survived), Pclass (1st, 2nd, 3rd), Name, Sex, Age, SibSp, Parch, Ticket, Fare, Cabin, Embarked  

## Steps Performed

1. **Load data into SQLite** – wrote `load_titanic.py` to create `titanic.db` with a `passengers` table.  
2. **Clean missing values** –  
   - Filled missing `Age` with the average age (29.7)  
   - Filled missing `Embarked` with the most common port 'S'  
   - Added `has_cabin` column (1 if cabin exists, else 0)  
   - Extracted `title` from `Name` (Mr, Mrs, Miss, etc.)  
3. **Analysis queries** – answered 5 business questions using SQL.  
4. **Export cleaned data** – saved to `titanic_cleaned.csv` and `titanic_cleaned.json`.

## Analysis Results

### 1. Survival Rate by Gender
| Sex    | Total | Survived | Survival Rate |
|--------|-------|----------|---------------|
| female | 314   | 233      | 74.2%         |
| male   | 577   | 109      | 18.9%         |

### 2. Survival Rate by Passenger Class

| Pclass | Total | Survived | Survival Rate |
|--------|-------|----------|---------------|
| 1      | 216    |  136    | 63.0%         |
| 2      | 184    |   87    | 47.3%         |
| 3      | 491    |  119    | 24.2%         |

### 3. Average Age of Survivors vs Non‑Survivors

| Survived | Average Age |
|----------|-------------|
| 0        | 30.415      |
| 1        | 28.550      |

### 4. Average Fare of Survivors vs Non‑Survivors

| Survived | Average Fare |
|----------|--------------|
| 0        |   22.118     |
| 1        |   48.395     |

### 5. Survival by Embarkation Port
| Port | Total | Survived | Survival Rate |
|------|-------|----------|---------------|
| C    | 168   | 93       | 55.4%         |
| Q    | 77    | 30       | 39.0%         |
| S    | 646   | 219      | 33.9%         |

## Files in this Folder
- `load_titanic.py` – loads CSV into SQLite.  
- `clean_titanic.py` – cleans missing values and adds columns.  
- `export_titanic.py` – exports cleaned data to CSV and JSON.  
- `titanic.db` – SQLite database (optional).  
- `titanic_cleaned.csv` – cleaned data as CSV.  
- `titanic_cleaned.json` – cleaned data as JSON.  
- `README.md` – this report.  
- `logbook.md` – daily progress log.

## How to Reproduce
1. Install Python 3.x.  
2. Ensure `titanic.csv` is in the same folder.  
3. Run `python load_titanic.py`.  
4. Run `python clean_titanic.py`.  
5. Run `python export_titanic.py`.  
6. Open `titanic_cleaned.csv` with Excel or any text editor.

## Challenges
The most difficult part was extracting titles from names, but using a `CASE` statement with `LIKE` patterns solved it cleanly.