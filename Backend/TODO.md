# TODO: Implement CSV Data Search for BSC CSIT and BIT Bots

## Steps to Complete:
- [x] Update dataloader.py to load CSV files and implement search functionality
- [x] Modify chatbot.py to integrate data loading and keyword-based search
- [x] Test the implementation to ensure department-specific access and search works
- [x] Verify no cross-access between BSC CSIT and BIT data

## Details:
- BSC CSIT bot loads and searches bsc_csit_data.csv
- BIT bot loads and searches bit_data.csv
- Search based on keywords from user message (case-insensitive match in any column)
- Append matching rows as context to the query for Ollama
- Tested data loading and search: BSC CSIT loaded 49 records, BIT 33; search works for keywords like 'programming' and 'algorithms'
- Chatbot integration tested; Ollama timeout noted but data search functional
