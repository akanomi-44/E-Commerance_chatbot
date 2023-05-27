# Apply chatGPT into Facebook's chatbot for E-commerce
Handle user requests:
1. Get recommendation (chatGPT)
2. Make orders
3. Contact human assistant
4. Answer to questions related to page's business field (chatGPT)
5. Get shop's location

## Deploy
1. Install packages
```
pip install -r requirements.txt
```
2. Create ```.env``` file from ```example.env```

3. Init template database
```python3 template.py```

4. Run
```hypercorn app:app```
