import codecs
import json


filenames = 'total.txt'
intents = ['search_almanac', 'qa_firstaid_treatment', 'capital', 'search', 'general_search']
rename_intents = ['search_almanac', 'qa_firstaid_treatment', 'search_capital', 'search_news', 'general_search']
# nums = ['100', '50', '5']
rename_domains_100 = ['huangli_100-1362948838480896000', 'jibing_100-1362963779678068736', 'shoudu_100-1363009765788008448', 'xinwen_100-1362971025342423040', 'tianqi_100-1362964723065118720']
rename_domains_50 = ['huangli_50-1362949324646834176', 'jibing_50-1362964399281672192', 'shoudu_50-1363010714585796608', 'xinwen_50-1362971796507201536', 'tianqi_50-1362968915859169280']
rename_domains_5 = ['huangli_5-1362949499880652800', 'jibing_5-1362964556333105152', 'shoudu_5-1363011111425675264', 'xinwen_5-1363008185919516672', 'tianqi_5-1362970384020725760']


def Name2lqd(path, filenames, rename_domain, rename_intents, intents):
    out_data = codecs.open(path + 'total_training_redomain_intent.txt', 'w', encoding='utf-8')
    with codecs.open(path+filenames, 'r', encoding='utf-8') as f:
        datas = f.readlines()
        for data in datas:
            context, domain, intent, con_slots = data.split()
            for i in range(5):
                if intent == intents[i]:
                    domain = rename_domain[i]
                    intent = rename_intents[i]
            re_data = context + '\t' + domain + '\t' + intent + '\t' + con_slots + '\n'
            out_data.write(re_data)
    out_data.close()


if __name__ == '__main__':
    Name2lqd(r'F:\git\MetaDialog\utils\\', filenames=filenames, rename_domain=rename_domains_5, rename_intents=rename_intents, intents=intents)