from flashtext import KeywordProcessor
import pandas as pd
from collections import defaultdict
from IPython.display import display, HTML

core_category_path = "Data/core_category.csv"
wikicssh_category_2_page_path = "Data/wikicssh_category_2_page.csv"
wikicssh_category_path = "Data/wikicssh_category.csv"
wikicssh_page_2_redirect = "Data/wikicssh_page_2_redirected.csv"



# print(processor.extract_keywords(text, span_info=True))
def get_html(text, processor):
    page2cats = (
        pd.read_csv(wikicssh_category_2_page_path)
            .groupby("page_title")
            .cat_title
            .agg(lambda x: list(x))
            .to_dict()
    )
    print("Hiii")
    spans = processor.extract_keywords(text, span_info=True)
    prev = 0
    parts = []
    category_counts = defaultdict(int)
    for entity, start, end in spans:
        if entity.startswith("Category:"):
            entity_cats = [entity.replace("Category:", "")]
        else:
            entity_cats = [c for c in page2cats.get(entity, [])]
        for cat in entity_cats:
            category_counts[cat] += 1
        if start > prev:
            parts.append(text[prev:start])
        parts.append(f"<a href='https://en.wikipedia.org/wiki/{entity}' title='{entity}'>{text[start:end]}</a>")
        prev = end
    tagged_doc = "".join(parts).replace("\n", "<br/>")
    pred_categories = " | ".join([
        f"<a href='https://en.wikipedia.org/wiki/Category:{k}' title='{k}'>{k}</a> ({v})"
        for k,v in sorted(category_counts.items(), key=lambda x: x[1], reverse=True)
    ])
    final_div = f"""<div>
    <div>
        <h3>Tagged document:</h3>
        {tagged_doc}
    </div>
    <div>
        <h3>Predicted categories:</h3>
        {pred_categories}
    </div>
    </div>"""
    return final_div

def get_final_data(final_text):
    print(final_text)


    print("yoyo")
    print(pd.read_csv(core_category_path).head())

    processor = KeywordProcessor()

    processor.add_keywords_from_dict(
        {
            f'Category:{k}': [f'{k.lower().replace("_", " ")}']
            for k in pd.read_csv(wikicssh_category_path).category.values
        }
    )

    for row in pd.read_csv(wikicssh_page_2_redirect).values:

        if isinstance(row[-1], float):
            row[-1] = row[0]
        processor.add_keyword(row[-1].lower().replace("_", " "), row[0])
        print("Hello")
    finalResult = get_html(final_text,processor)
    print(finalResult)
    return finalResult
