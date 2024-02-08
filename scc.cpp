#include <bits/stdc++.h>
using namespace std;
#define ll long long int
#define ld long double
#define mp make_pair
#define pb push_back
#define pll pair<ll,ll>

ll INF = 1000000007;

vector<ll>adj[100005];
vector<ll>tra[100005];
vector<ll>component;
ll vis[100005]={0};
vector<ll>order;


//-----------------//
  #define amin main
//-----------------//



void dfs1 (ll v) 
{
    vis[v] = 1;
    for (ll i=0; i<(ll)adj[v].size(); i++)
     {
            if (vis[adj[v][i]]==0)
                dfs1 (adj[v][i]);
     }
    order.push_back (v);

 	return;
}

void dfs2 (ll v)
{
        vis[v] = 1;
        component.push_back (v);
        for (ll i=0; i<(ll)tra[v].size();i++)
        {
            if (vis[tra[v][i]]==0)
                dfs2 (tra[v][i]);
        }
}


int amin()
{
	 	freopen("input1.txt", "r", stdin);
     	freopen("output1.txt", "w", stdout);
		ios_base::sync_with_stdio(false);
		cin.tie(NULL);
		ll i,j;
		
		ll n = (100-80+1)*(100-80+1);
		// cout<<n<<endl;
		ll edges;
		cin>>edges;
		for(i=0;i<edges;i++)
		{
			ll a,b;
			cin>>a>>b;
			adj[a].pb(b);
			tra[b].pb(a);
		}
		memset(vis,0,sizeof(vis));

		for(i=80;i<=100;i++)
		{
			for(j=80;j<=100;j++)
			{
				ll k = i + j*100;
				if(vis[k]==0)
				{
					dfs1(k);
				}
			}
		}
		memset(vis,0,sizeof(vis));

		j= 0;
		ll cnt= 1;
		for(i=80;i<=100;i++)
		{
			for(ll x=80;x<=100;x++)
			{

				ll v = order[n-1-j];
				if(vis[v]==0)
				{
					dfs2(v);
					cout<<"-"<<endl;
					for(ll k=0 ;k<(ll)component.size();k++)
					{
						cout<<component[k]<<endl;
					}
					cnt++;
					component.clear();
				}
				j++;
			}
		}

	return 0;
}
