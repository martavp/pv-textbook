clear all;

% Program that integrates the EQE to get the Jsc

%Tommamos la EQE del fichero de ref
% SR (A/W)= EQE(lambda)*lambda(nm)/1239.8

%close all;
%clear all%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%% EQE2Jsc %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


% Definimos las constantes necesarias
q   = 1.602177e-19;         % Carga e-              (Q)
h   = 6.6260755e-34;        % Cte de Plank;         (Js)
c   = 299792458;            % velocidad de la luz   (m/s)


%Cargamos el espectro sobre el que queremos integrar la corrient
E_AM0=load ('C:\work\EQE2Jsc\eqe2\AM0_new.si');
EQE_sample=load('C:\Pilar\Caltech_Projects\LIBRO\Problems\EQE_BC_BOL.txt');

lambda_espectro_AM0 = E_AM0(:,1);
intensidad_espec_AM0= E_AM0(:,2);

% Cargamos la respuesta espectral que queremos escalar
lambda_sr_AM0 = EQE_sample(:,1); %nm
value_sr_AM0  = EQE_sample(:,2).*lambda_sr_AM0*(1e-10*q/h/c);  %  (A/Wnm)

% Elegimos el intervalo de lambdas ms adecuado para la interpolacin

lambda_0_AM0 = max ([min(lambda_sr_AM0) min(lambda_espectro_AM0)]);
lambda_AM0   = [lambda_0_AM0:1:max(lambda_sr_AM0)];

lambda_AM0_int   = [lambda_0_AM0:5:max(lambda_sr_AM0)];


% Aqui interpolamos
int_eqe_AM0       = interp1 (EQE_sample(:,1), EQE_sample(:,2),lambda_AM0_int);


int_sr_AM0       = interp1 (lambda_sr_AM0, value_sr_AM0,lambda_AM0);
int_espectro_AM0 = interp1 (lambda_espectro_AM0, intensidad_espec_AM0,lambda_AM0, 'linear','extrap');

data_EQE_interp(:,1)=lambda_AM0_int;
data_EQE_interp(:,2)=int_eqe_AM0;

%plot(data_EQE_interp(:,1),data_EQE_interp(:,2), '*')
%figure(1)
%plot(EQE_sample(:,1), T_CG(:,1),'*')
figure(2)
plot(EQE_sample(:,1),EQE_sample(:,2), '*')


% Realizamos la integral:
%            f 
%   JSC =    | (SR*Espectro) dlambda
%            j
%

Jsc_AM0 = trapz (lambda_AM0, int_espectro_AM0.*int_sr_AM0)

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%% AM1.5G %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%Cargamos el espectro sobre el que queremos integrar la corrient
E_AM15G = load ('C:\work\EQE2Jsc\eqe2\am15g_i_1000wm2.si');

lambda_espectro_AM15G = E_AM15G(:,1);
intensidad_espec_AM15G= E_AM15G(:,2);

% Cargamos la respuesta espectral que queremos escalar
lambda_sr_AM15G = EQE_sample(:,1); %nm
value_sr_AM15G  = EQE_sample(:,2).*lambda_sr_AM15G*(1e-10*q/h/c);  %  (A/Wnm)

% Elegimos el intervalo de lambdas ms adecuado para la interpolacin

lambda_0_AM15G = max ([min(lambda_sr_AM15G) min(lambda_espectro_AM15G)]);
lambda_AM15G   = [lambda_0_AM15G:1:max(lambda_sr_AM15G)];


% Aqui interpolamos
int_sr_AM15G       = interp1 (lambda_sr_AM15G, value_sr_AM15G,lambda_AM15G);
int_espectro_AM15G = interp1 (lambda_espectro_AM15G, intensidad_espec_AM15G,lambda_AM15G, 'linear','extrap');

Jsc_AM15G = trapz (lambda_AM15G, int_espectro_AM15G.*int_sr_AM15G)

