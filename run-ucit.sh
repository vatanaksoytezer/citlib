read -p 'Please enter the name of the graph: ' graph_name

graph_name+=".lp"
# Search for the graph in file path
if true # [[ -n $(find -name "$graph_name" -mmin -1) ]]
then
    clingo -n 0 $graph_name reachability.lp
fi