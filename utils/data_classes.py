from dataclasses import dataclass


@dataclass
class ParsingConfig:
    url: str

    @property
    def parsing_url(self) -> str:
        return self.url


@dataclass
class DatabaseConfig:
    login: str
    password: str
    server: str
    port: int
    name: str

    @property
    def db_connection(self) -> str:
        return f'postgresql://{self.login}:{self.password}@' \
               f'{self.server}:{self.port}/{self.name}'


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
    amount: int
