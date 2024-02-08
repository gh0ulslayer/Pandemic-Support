#include <bits/stdc++.h>
using namespace std;
#define ll long long int
#define ld long double
#define mp make_pair
#define pb push_back
#define pll pair<ll,ll>

ll INF = 1000000007;


//-----------------//
  #define amin main
//-----------------//

vector<pair<ll,pair<ll,ll>>>adj;
ll parent[100000];
ll ranki[100000];

int find_set(int v) {
    if (v == parent[v])
        return v;
    return parent[v] = find_set(parent[v]);
}

void union_sets(int a, int b) {
    a = find_set(a);
    b = find_set(b);
    if (a != b) {
        if (ranki[a] < ranki[b])
            swap(a, b);
        parent[b] = a;
        if (ranki[a] == ranki[b])
            ranki[a]++;
    }
}


int amin()
{
	 	freopen("input.txt", "r", stdin);
        freopen("output.txt", "w", stdout);
		ios_base::sync_with_stdio(false);
		cin.tie(NULL);
		ll i;
		ll edges;
		cin>>edges;
		for(i=0;i<edges;i++)
		{
			ll u,v,w;
			cin>>u>>v>>w;
			adj.pb({w,{u,v}});
		}
		for(i=0;i<100000;i++)
		{
			parent[i]=i;
			ranki[i]=i;
		}
		sort(adj.begin(),adj.end());
		ll cost = 0;
		vector<pll>ans;
		for(i=0;i<(ll)adj.size();i++)
		{
			ll u = adj[i].second.first;
			ll v = adj[i].second.second;
			ll w  = adj[i].first;
			if(find_set(u)!=find_set(v))
			{
				cost += w;
				ans.pb({u,v});
				union_sets(u,v);
			}

		}
		for(i=0;i<(ll)ans.size()-1;i++)
		{
			cout<<ans[i].first<<" "<<ans[i].second<<' ';
		}
		cout<<ans[i].first<<" "<<ans[i].second;
	return 0;
}
