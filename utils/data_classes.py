from dataclasses import dataclass


@dataclass
class ParsingConfig:
    url: str

    @property
    def parsing_url(self) -> str:
        return self.url


@dataclass
class DatabaseConfig:
    user: str
    password: str
    host: str
    port: int
    name: str

    @property
    def db_connection(self) -> str:
        return f'postgresql://{self.user}:{self.password}@' \
               f'{self.host}:{self.port}/{self.name}'


@dataclass
class APIConfig:
    cookie: str
    port: int

    @property
    def api_cookie(self) -> str:
        return self.cookie

    @property
    def api_port(self) -> int:
        return self.port


@dataclass
class TableRow:
    begin_ip: str
    end_ip: str
    amount: str

    def get_values(self) -> list:
        return [self.begin_ip, self.end_ip, self.amount]
