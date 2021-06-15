import pandas as pd
import networkx as nx
from collections import OrderedDict


def show_context_of_category(node, cat2pages, G):
    parents = list(G.predecessors(node))
    children = list(G.neighbors(node))
    table_header = """
 
    <thead><tr><th>Parents</th><th>Node</th><th>Children</th></tr></thead>
    """
    parents_list = "\n".join(
        [f"<li><a href='https://en.wikipedia.org/wiki/Category:{i}'>{i}</a></li>" for i in parents])
    children_list = "\n".join(
        [f"<li><a href='https://en.wikipedia.org/wiki/Category:{i}'>{i}</a></li>" for i in children])
    node_list = f"<li><a href='https://en.wikipedia.org/wiki/Category:{node}'>{node}</a></li>"
    page_list = " | ".join([
        f"<a href='https://en.wikipedia.org/wiki/{i}'>{i}</a>"
        for i in cat2pages[node]
    ])
    table_body = f"""
       
    <tbody>
    <tr>
        <td><ul>{parents_list}</ul></td>
        <td style='background-color: pink'>{node_list}</td>
        <td><ul>{children_list}</ul></td>
    </tr>
    </tbody>"""

    div = f"""
     <!DOCTYPE html>
     <html>
     <head>
    <style>
table {{
  font-family: arial, sans-serif;
  border-collapse: collapse;
  width: 100%;
}}

td, th {{
  border: 1px solid #dddddd;
  text-align: left;
  padding: 8px;
}}

tr:nth-child(even) {{
  background-color: #dddddd;
}}
</style>
</head>
<body>
    <div>
    <table>{table_header}{table_body}</table>
    </div>
"""
    return div


def show_graph_of_category(node, G):
    parents = list(G.predecessors(node))
    children = list(G.neighbors(node))
    parents_lists = ""
    children_lists = ""
    parents_link_list = ""
    children_link_lists = ""
    for i in parents:
        parents_lists += "{" + "'id':'" + i + "'," + "'group':" + "1" + "},"
        parents_link_list += "{" + "'source':'" + i + "'," + "'target':'" + node + "','value': 80},"
    for i in children:
        children_lists += "{" + "'id':'" + i + "'," + "'group':" + "3" + "},"
        children_link_lists += "{" + "'source':'" + i + "'," + "'target':'" + node + "','value': 80},"
    parents_lists = parents_lists[:-1]
    children_lists = children_lists[:-1]
    node_list = "{" + "'id':'" + node + "'," + "'group':" + "2" + "}"
    all_nodes = str(parents_lists) + ',' + str(children_lists) + "," + str(node_list)
    all_links = str(parents_link_list[:-1]) + ',' + str(children_link_lists[:-1])

    graph_code = """

    <style>

    .link line {
      stroke: #999;
      stroke-opacity: 0.6;
    }

    .labels text {
      pointer-events: none;
      font: 10px sans-serif;
    }

    </style>



    <svg width="1200" height="800"></svg>
    <script src="https://d3js.org/d3.v4.min.js"></script>
    <script src="https://bl.ocks.org/jpurma/raw/6dd2081cf25a5d2dfcdcab1a4868f237/d3-ellipse-force.js"></script>
    <script> """ + f""" var graph = {{
      "nodes": [
      {all_nodes}

      ],
      "links": [
      {all_links}
      ]
    }}
    </script>
    """ + """<script>

    var svg = d3.select("svg"),
        width = +svg.attr("width"),
        height = +svg.attr("height");

    var color = d3.scaleOrdinal(d3.schemeCategory20);

    var nd;
    for (var i=0; i<graph.nodes.length; i++) {
      nd = graph.nodes[i];
      nd.rx = nd.id.length * 4.5; 
      nd.ry = 12;
    } 

    var simulation = d3.forceSimulation()
        .force("link", d3.forceLink().id(function(d) { return d.id; }))
        .force("collide", d3.ellipseForce(6, 0.5, 5))
        .force("center", d3.forceCenter(width / 2, height / 2));

    var link = svg.append("g")
        .attr("class", "link")
      .selectAll("line")
      .data(graph.links)
      .enter().append("line")
        .attr("stroke-width", function(d) { return Math.sqrt(d.value); });

    var node = svg.append("g")
        .attr("class", "node")
      .selectAll("ellipse")
      .data(graph.nodes)
      .enter().append("ellipse")  
        .attr("rx", function(d) { return d.rx; })
        .attr("ry", function(d) { return d.ry; })
        .attr("fill", function(d) { return color(d.group); })
        .call(d3.drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended));

    var text = svg.append("g")
        .attr("class", "labels")
      .selectAll("text")
      .data(graph.nodes)
      .enter().append("text")  
        .attr("dy", 2)
        .attr("text-anchor", "middle")
        .text(function(d) {return d.id})
        .attr("fill", "white");


    simulation
      .nodes(graph.nodes)
      .on("tick", ticked);

    simulation.force("link")
         .links(graph.links);

    function ticked() {
      link
          .attr("x1", function(d) { return d.source.x; })
          .attr("y1", function(d) { return d.source.y; })
          .attr("x2", function(d) { return d.target.x; })
          .attr("y2", function(d) { return d.target.y; });

      node
          .attr("cx", function(d) { return d.x; })
          .attr("cy", function(d) { return d.y; });
      text
          .attr("x", function(d) { return d.x; })
          .attr("y", function(d) { return d.y; });

    }

    function dragstarted(d) {
      if (!d3.event.active) simulation.alphaTarget(0.3).restart();
      d.fx = d.x;
      d.fy = d.y;
    }

    function dragged(d) {
      d.fx = d3.event.x;
      d.fy = d3.event.y;
    }

    function dragended(d) {
      if (!d3.event.active) simulation.alphaTarget(0);
      d.fx = null;
      d.fy = null;
    }

    </script>
    </body>
</html>
    """

    return graph_code


def get_final_page():
    df_categories = pd.read_csv('Data/wikicssh_category.csv')
    df_categories.head()

    df_categories.set_index("category").head().to_dict(orient="index", into=OrderedDict)

    df_category_links = pd.read_csv('Data/wikicssh_category_links.csv')
    df_category_links.head()

    df_pages = pd.read_csv('Data/wikicssh_category_2_page.csv')
    df_pages.head()

    df_redirects = pd.read_csv('Data/wikicssh_page_2_redirected.csv')
    df_redirects.head()

    isolate_cats = (
            set(df_categories.category.values)
            - set(
        set(df_category_links.parent_cat.values)
        | set(df_category_links.child_cat.values)
    )
    )

    root_child_cats = set(
        set(df_category_links.parent_cat.values)
        - set(df_category_links.child_cat.values)
    )

    df_category_links_all = pd.concat([
        df_category_links,
        df_categories[df_categories.category.isin(root_child_cats)].rename(columns={
            "category": "child_cat",
            "level": "child_level",  # parent_level	child_level
        }).assign(parent_cat="<ROOT>", parent_level=0),
        pd.DataFrame({
            "parent_cat": [""],
            "child_cat": ["<ROOT>"],
            "parent_level": [-1],
            "child_level": [0],
        })
        #     df_categories[df_categories.category.isin(isolate_cats)].rename(columns={
        #         "category": "child_cat",
        #         "level": "child_level", #	parent_level	child_level
        #     }).assign(parent_cat="", parent_level=0)

    ], axis=0, sort=True).sort_values(["parent_level", "child_level"])
    df_category_links_all.shape
    print("list all links")
    print(df_category_links_all.child_cat)

    df_category_links_all[
        # (df_category_links_all.parent_cat=="Artificial_intelligence")
        (df_category_links_all.child_cat == "Artificial_intelligence")
    ]
    print("list all links with AI")
    print(df_category_links_all)
    G = nx.DiGraph()

    G.add_edges_from(
        df_category_links_all.set_index(["parent_cat", "child_cat"]).to_dict(orient="index", into=OrderedDict))
    G.size()

    nx.algorithms.is_directed_acyclic_graph(G)

    node = "Artificial_intelligence"
    list(G.neighbors(node))

    cat2pages = pd.read_csv('Data/wikicssh_category_2_page.csv').groupby("cat_title").page_title.agg(list)
    return show_context_of_category(node, cat2pages, G) + show_graph_of_category(node, G)


print(get_final_page())