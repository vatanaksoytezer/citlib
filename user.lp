% ##import(citlib.flow)
% ##import(citlib.graphs.c)
% ##import(citlib.any,t=2)
##import(citlib.reachability)
% ##import(citlib.order,t=2)
% TODO: We may want nonconsec to call any as a dependency
% ##import(citlib.nonconsec,t=2)
% ##import(citlib.all-entity)
##import(citlib.ordernew,t=2)
% Set timeout for clingo

% Make this generic, key value dictionary for any variable
##define timeout=2

% #show flow/3.
