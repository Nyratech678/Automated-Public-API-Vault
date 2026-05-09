from src.writer import export_for_site, write_readmes


def run(categorized):
    counts = write_readmes(categorized)
    export_for_site(categorized)
    return counts
