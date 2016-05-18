/// <reference path="./../typings/main.d.ts" />


export interface Links {
    related: string;
}

export interface Relationships {
}

export interface Attributes {
}

export interface JsonAPISingleRespons {
    relationships: Relationships;
    id: string;
    type: string;
    attributes: Attributes;
}

export interface JsonAPIManyRespons {
    data: JsonAPISingleRespons[];
}