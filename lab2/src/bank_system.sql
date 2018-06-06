/*==============================================================*/
/* DBMS name:      MySQL 5.0                                    */
/* Created on:     2018/6/5 20:49:26                            */
/*==============================================================*/


drop table if exists 储蓄账户;

drop table if exists 共有;

drop table if exists 员工;

drop table if exists 客户;

drop table if exists 拥有;

drop table if exists 支付情况;

drop table if exists 支票账户;

drop table if exists 支行;

drop table if exists 负责;

drop table if exists 账户;

drop table if exists 贷款;

/*==============================================================*/
/* Table: 储蓄账户                                                  */
/*==============================================================*/
create table 储蓄账户
(
   账户号                  varchar(128) not null,
   支行名                  varchar(128),
   余额                   float not null,
   开户日期                 date not null,
   利率                   float not null,
   货币类型                 varchar(128) not null,
   primary key (账户号)
);

/*==============================================================*/
/* Table: 共有                                                    */
/*==============================================================*/
create table 共有
(
   贷款号                  varchar(128) not null,
   客户身份证号               varchar(128) not null,
   primary key (贷款号, 客户身份证号)
);

/*==============================================================*/
/* Table: 员工                                                    */
/*==============================================================*/
create table 员工
(
   员工身份证号               varchar(128) not null,
   支行名                  varchar(128) not null,
   部门经理身份证号           varchar(128),
   姓名                   varchar(128) not null,
   电话                   varchar(128) not null,
   家庭住址                 varchar(128),
   入职日期                 date not null,
   primary key (员工身份证号)
);

/*==============================================================*/
/* Table: 客户                                                    */
/*==============================================================*/
create table 客户
(
   客户身份证号               varchar(128) not null,
   姓名                   varchar(128) not null,
   联系电话                 varchar(128) not null,
   家庭住址                 varchar(128),
   联系人姓名                varchar(128) not null,
   联系人手机号               varchar(128) not null,
   联系人email             varchar(128),
   关系                   varchar(128) not null,
   primary key (客户身份证号)
);

/*==============================================================*/
/* Table: 拥有                                                    */
/*==============================================================*/
create table 拥有
(
   客户身份证号               varchar(128) not null,
   账户号                  varchar(128) not null,
   最近访问日期               date not null,
   primary key (客户身份证号, 账户号)
);

/*==============================================================*/
/* Table: 支付情况                                                  */
/*==============================================================*/
create table 支付情况
(
   支付日期                 date not null,
   贷款号                  varchar(128) not null,
   支付金额                 float not null,
   primary key (支付日期,贷款号)
);

/*==============================================================*/
/* Table: 支票账户                                                  */
/*==============================================================*/
create table 支票账户
(
   账户号                  varchar(128) not null,
   支行名                  varchar(128),
   余额                   float not null,
   开户日期                 date not null,
   利率                   float not null,
   货币类型                 varchar(128) not null,
   透支额                  float not null,
   primary key (账户号)
);

/*==============================================================*/
/* Table: 支行                                                    */
/*==============================================================*/
create table 支行
(
   支行名                  varchar(128) not null,
   城市                   varchar(128) not null,
   资产                   float not null,
   primary key (支行名)
);

/*==============================================================*/
/* Table: 负责                                                    */
/*==============================================================*/
create table 负责
(
   员工身份证号               varchar(128) not null,
   客户身份证号               varchar(128) not null,
   负责人类型                varchar(128) not null,
   primary key (员工身份证号, 客户身份证号,负责人类型)
);

/*==============================================================*/
/* Table: 账户                                                    */
/*==============================================================*/
create table 账户
(
   账户号                  varchar(128) not null,
   支行名                  varchar(128) not null,
   余额                   float not null,
   开户日期                 date not null,
   primary key (账户号)
);

/*==============================================================*/
/* Table: 贷款                                                    */
/*==============================================================*/
create table 贷款
(
   贷款号                  varchar(128) not null,
   支行名                  varchar(128) not null,
   总金额                  float not null,
   当前状态                varchar(128) not null,
   primary key (贷款号)
);

alter table 储蓄账户 add constraint FK_Inheritance_2 foreign key (账户号)
      references 账户 (账户号) on delete restrict on update restrict;

alter table 共有 add constraint FK_共有 foreign key (贷款号)
      references 贷款 (贷款号) on delete restrict on update restrict;

alter table 共有 add constraint FK_共有2 foreign key (客户身份证号)
      references 客户 (客户身份证号) on delete restrict on update restrict;

alter table 员工 add constraint FK_工作 foreign key (支行名)
      references 支行 (支行名) on delete restrict on update restrict;

alter table 员工 add constraint FK_经理 foreign key (部门经理身份证号)
      references 员工 (员工身份证号) on delete restrict on update restrict;

alter table 拥有 add constraint FK_拥有 foreign key (客户身份证号)
      references 客户 (客户身份证号) on delete restrict on update restrict;

alter table 拥有 add constraint FK_拥有2 foreign key (账户号)
      references 账户 (账户号) on delete restrict on update restrict;

alter table 支付情况 add constraint FK_逐次支付 foreign key (贷款号)
      references 贷款 (贷款号) on delete restrict on update restrict;

alter table 支票账户 add constraint FK_Inheritance_1 foreign key (账户号)
      references 账户 (账户号) on delete restrict on update restrict;

alter table 负责 add constraint FK_负责 foreign key (员工身份证号)
      references 员工 (员工身份证号) on delete restrict on update restrict;

alter table 负责 add constraint FK_负责2 foreign key (客户身份证号)
      references 客户 (客户身份证号) on delete restrict on update restrict;

alter table 账户 add constraint FK_开户 foreign key (支行名)
      references 支行 (支行名) on delete restrict on update restrict;

alter table 贷款 add constraint FK_发放 foreign key (支行名)
      references 支行 (支行名) on delete restrict on update restrict;

