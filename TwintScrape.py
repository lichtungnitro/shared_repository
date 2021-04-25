import twint

c = twint.Config()

c.Limit = 10
c.Search = "Nevigate"
c.Store_csv = True
c.Output = "/Users/nitrolichtung/Downloads/test.csv"
c.Lang = "en"

c.Proxy_host = "127.0.0.1"
c.Proxy_port = 7890
c.Proxy_type = "http"

twint.run.Search(c)