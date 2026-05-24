import logging
import glob
import os
from summarizer import read_file, summarize_with_retry  # reuse existing functions

logging.basicConfig(
    filename='summarizer.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
 
def batch_summarize():
    folder = input("Enter folder path: ")
    txt_files = glob.glob(os.path.join(folder, "*.txt"))
    if not txt_files:
        logging.info("No .txt files found.")
        return
    
    output_dir = "./summaries"
    os.makedirs(output_dir, exist_ok=True)
    success = 0
    failed = 0
    for i, file_path in enumerate(txt_files, 1):
        filename = os.path.basename(file_path)
        logging.info(f"Processing file {i} of {len(txt_files)}: {filename}")
        print(f"Processing {filename} ")
        text = read_file(file_path)   # your existing function
        if text is None:
            logging.info(f"Could not read {filename}")
            failed += 1
            continue
        
        try:
            summary = summarize_with_retry(text)   # your existing function
            out_name = os.path.splitext(filename)[0] + "_summary.txt"
            out_path = os.path.join(output_dir, out_name)
            with open(out_path, 'w', encoding='utf-8') as f:
                f.write(summary)
            logging.info(f"  -> Saved to {out_path}")
            success += 1
        except Exception as e:
            logging.error(f"  -> Failed: {e}")
            failed += 1
            print(f"Failed to summarize {filename}: {e}")
    
    logging.info(f"Batch completed: {success} succeeded, {failed} failed")

if __name__ == "__main__":
    batch_summarize()