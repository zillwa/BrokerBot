from DataHandler import AlpacaDataHandler
from ExecutionHandler import AlpacaExecutionHandler
import threading
from multiprocessing import Process, Pipe


"""
    Overview:
        class that handles running our different strategies, using DH & EH's that are 
        customized to what ever api constructed with
    TODO:
        construct proper DH, and EH for whatever APi selected
            select from avaliable DH's ex binance DH, alpaca DH, .. ect.
        decide what fucntion/ stratey its running
            ex. longterm, short term, medium term... ect.
        instanciate member variables    
            log(Data structure communicating with the DH)
            DH
            EH
    """
class StrategyHandler:
    #====================Creators====================
    """
    Overview: High-Risk Strategy will be implemented here. Below is just an example to give an idea. 

    Requires:   api_key,secret_key,base_url,data_url,socket, base_url, ticker,
                DH_API,EH_API,

    Modifies: DH, EH,log,
    Effects: DH is initialized, EH is initialized, stream is listend to, Log is initialized.
    Returns: none
    """
    def __init__(self, api_key, secret_key, base_url, socket, strategy): 
        self.strategy = strategy
        self.DataHandler = AlpacaDataHandler(
            api_key, secret_key, base_url, socket)
        self.ExecutionHandler = AlpacaExecutionHandler(
            api_key, secret_key, base_url)

        self.dh_conn = None
        self.eh_conn = None
    #====================Observers====================
    """
    Overview: tests & prints if we revieved a message from the DH

    Requires: none
    Modifies: none
    Effects: none
    Returns: none
    Throws: none
    """
    def test_recv_dh(self):
        while True:
            data = self.dh_conn.recv()
            print(f"SH RECV: {data}")
    #====================Producers====================
    #====================Mutators====================


    """
    Example Trading strategy
        def shortTerm(ticker):
            listen to stream of ticker\            
                    start adding to the message log
            while(true):
                add to the message log
                stat calculations for the strategy
                calculate trade signal 
                EH.enterTrade(ticker, signal)
                while(order has not been fullfilled){
                    // check if order fullfuill has been recieved
                    // add to log
                    //continue contiuous calculations
                }
                begin dynamic stop loss caluclations, by continuing the technical indicator calculations
                stoploss();
    """
        
    """
    Overview: High-Risk Strategy will be implemented here. Below is just an example to give an idea. 

    Requires: bars is non-null
    Modifies: none
    Effects: none
    Returns: sell-trade decision if previous close is less than fibonacci value AND current open is less than fibonacci value, else returns none representing no decision is made
    """
    def HighRisk(symbol, bars):
        fib_values = self.fibonacci(symbol, bars)
        # elif current_price == fib_values[]
        for fib_val in fib_values:
            if previous_close < fib_val and current_open < fib_val:
                # by returning 'SHORT', this will tell execution handler to make a short trade
                decision = ["SHORT", None, None]
                return decision 
        return None
    
    """
    Overview: Medium-Risk Strategy will be implemented here. Below is just an example to give an idea. 

    Requires: bars is non-null
    Modifies: none
    Effects: none
    Returns: buy-trade decision, take-profit, and stop-loss if current volume is 1.5x greater than previous volume. 
    """
    def MidRisk(bars):
        pass

    """
    Overview: Low-Risk Strategy will be implemented here. Below is just an example to give an idea. 

    Requires: bars is non-null
    Modifies: none
    Effects: none
    Returns: buy-trade decision, take-profit, and stop-loss if current volume is 1.5x greater than previous volume. 
    """
    def LowRisk(symbol, bars):
        vol_1 = self.volume(bars[0])
         # I think each bar should be tuple with open, close, low, high, current prices & volume 
        vol_2 = self.volume(bars[1])

        if vol_1 > (vol_2 * 1.5):
            fib_values = self.fibonacci(symbol, bars)
            TP = fib_values[3]  # take profit is the 3rd retracement
            SL = fib_values[2]  # stop loss is the 2nd retracement
            decision = ["BUY", TP, SL]
            return decision 
    
    """
    Overview: calculates the fibonacci values of 23.6%, 38.2%, 50%, 61.8%, and 78.6% 

    Requires: bars is non-null
    Modifies: none
    Effects: none
    Returns: fibonacci values 
    Throws: RunTimeException if bars or symbol is null
    """
    def fibonacci(symbol, bars):
        if symbol is None or bars is None:
            raise RuntimeError('fibonacci called with a null') from exc
        # first data-value in the bars array (most recent bar to current bar)
        first = bars[0]
        # last data-value in the bars array (most farthest bar to current bar)
        second = bars[len(candles) - 1]
        retracements = [0.236, 0.382, 0.5, 0.618, 0.786]
        fib_values = [(second - ((second - first) * retracement))
                      for retracement in retracements]
        return fib_values 
    """
    Overview: sets the pipe connections

    Requires: none
    Modifies: none
    Effects: none
    Returns: none
    Throws: RunTimeError if any of the parameters are null
    """
    def set_pipe_conns(self, dh_conn, eh_conn):
        if dh_conn is None or eh_conn is None:
            raise RuntimeError('set_pipe_conns called with a null') from exc
        self.dh_conn = dh_conn
        self.eh_conn = eh_conn
    """
    Overview: Create DH + EH process and pipe connection points for both

    Requires: none
    Modifies: DataHandler,
    Effects: DataHandeler starts a stream on ticket "TSLA"
    Returns: none
    Throws: none
    TODO: figure out best way to pass these pipe connections points to DH and EH
    TODO: add logic in SH and EH for using pipe to communication with SH
    """
    def run(self):
        sh_dh_conn, dh_sh_conn = Pipe()
        sh_eh_conn, eh_sh_conn = Pipe()

        self.set_pipe_conns(sh_dh_conn, sh_eh_conn)
        # Set pipe conn in DH
        self.DataHandler.set_pipe_conn(dh_sh_conn)

        dh_listen_proc = Process(
            target=self.DataHandler.start_streaming, args=("TSLA",))

        dh_listen_proc.start()
        self.test_recv_dh()
