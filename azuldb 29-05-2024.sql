-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 30-05-2024 a las 00:10:05
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `azuldb`
--

DELIMITER $$
--
-- Procedimientos
--
CREATE DEFINER=`ticscode`@`%` PROCEDURE `spActualizarCliente` (IN `p_id_cliente` INT, IN `p_nombres` VARCHAR(60), IN `p_direccion` VARCHAR(60), IN `p_telefono` VARCHAR(10), IN `p_email` VARCHAR(128))   UPDATE cliente as c SET c.nombres=p_nombres, c.direccion=p_direccion, c.telefono=telefono,
c.email=p_email WHERE c.idCliente=p_id_cliente$$

CREATE DEFINER=`ticscode`@`%` PROCEDURE `spActualizarOrden` (IN `p_id_orden` INT, IN `p_id_cliente` INT, IN `p_fecha_pedido` DATE, IN `p_fecha_entrega` DATE, IN `p_estado` VARCHAR(50), IN `p_saldo` FLOAT, IN `p_total` FLOAT, IN `p_id_usuario` INT, IN `p_observacion` TEXT)   UPDATE orden_trabajo SET id_cliente=p_id_cliente, fecha_pedido=p_fecha_pedido, fecha_entrega=p_fecha_entrega, estado=upper(p_estado),
saldo=p_saldo, total=p_total, id_usuario=p_id_usuario, observacion=p_observacion
WHERE id_orden=p_id_orden$$

CREATE DEFINER=`ticscode`@`%` PROCEDURE `spActualizarProducto` (IN `p_id_producto` INT, IN `p_descripcion` VARCHAR(180), IN `p_cantidad` INT, IN `p_stock` INT, IN `p_precio` FLOAT, IN `p_obs` TEXT)   UPDATE producto SET descripcion=upper(p_descripcion), cantidad=p_cantidad,
stock=p_stock, precio=p_precio, observacion=upper(p_obs)
WHERE id_producto=p_id_producto$$

CREATE DEFINER=`ticscode`@`%` PROCEDURE `spActualizarTipoPrenda` (IN `p_id_prenda` INT, IN `p_descripcion` VARCHAR(180), IN `p_id_servicio` INT, IN `p_precio` FLOAT)   update tipo_prenda as tp set tp.descripcion=p_descripcion, tp.precio=p_precio,
tp.id_servicio=p_id_servicio where tp.id_prenda=p_id_prenda$$

CREATE DEFINER=`ticscode`@`%` PROCEDURE `spAgregarPrenda` (IN `id_prenda` INT, IN `id_servicio` INT, IN `p_cantidad` INT, IN `precio` FLOAT, IN `p_observacion` TEXT, IN `p_id_orden` INT)   INSERT INTO prenda (id_tipo_prenda, id_servicio, cantidad, precio_total,
                    observacion, id_orden)
VALUES(id_prenda, id_servicio, p_cantidad, precio, p_observacion,
       p_id_orden)$$

CREATE DEFINER=`ticscode`@`%` PROCEDURE `spAgregarProducto` (IN `p_descripcion` VARCHAR(180), IN `p_cantidad` INT, IN `p_stock` INT, IN `p_precio` FLOAT, IN `p_observacion` TEXT)   IF EXISTS(SELECT * FROM producto AS p WHERE p.descripcion=p_descripcion) THEN
	SELECT 0;
ELSE
	INSERT INTO producto(descripcion, cantidad, stock, precio, observacion)
    VALUES (p_descripcion, p_cantidad, p_stock, p_precio, p_observacion);
    
    SELECT id_producto FROM producto WHERE descripcion=p_descripcion;
END IF$$

CREATE DEFINER=`ticscode`@`%` PROCEDURE `spAgregarTipoPrenda` (IN `p_descripcion` VARCHAR(180), IN `p_precio` FLOAT, IN `p_id_servicio` INT)   BEGIN
    if exists(select * from tipo_prenda where descripcion=p_descripcion) then
        SELECT 0;
    else
        insert into tipo_prenda(descripcion, precio, id_servicio) 
        values(upper(p_descripcion), p_precio, p_id_servicio);
        SELECT LAST_INSERT_ID();
    end if;
end$$

CREATE DEFINER=`ticscode`@`%` PROCEDURE `spBuscarCliente` (IN `texto` VARCHAR(10))   SELECT * FROM cliente AS c WHERE c.cedula=texto OR c.nombres like concat('%', texto, '%')$$

CREATE DEFINER=`ticscode`@`%` PROCEDURE `spClientesRegistrados` ()   SELECT * FROM cliente as c$$

CREATE DEFINER=`ticscode`@`%` PROCEDURE `spContarOrdenes` ()   BEGIN
	DECLARE cont int;
    SELECT COUNT(*)	INTO cont FROM
		orden_trabajo;
    IF cont=0 THEN
    	SET cont=1217014;
        SELECT cont;
    ELSE
    	SELECT o.id_orden+1 FROM orden_trabajo as o ORDER BY o.id_orden DESC LIMIT 1;
    END IF;
END$$

CREATE DEFINER=`ticscode`@`%` PROCEDURE `spEliminarProducto` (IN `p_id_producto` INT)   DELETE FROM producto WHERE id_producto=p_id_producto$$

CREATE DEFINER=`ticscode`@`%` PROCEDURE `spEliminarTipoPrenda` (IN `p_id_prenda` INT)   DELETE FROM tipo_prenda  WHERE id_prenda=p_id_prenda$$

CREATE DEFINER=`ticscode`@`%` PROCEDURE `spFiltrarCatalogo` (IN `texto` VARCHAR(180))   SELECT tp.id_prenda, tp.descripcion, tp.precio, ts.descripcion as servicio from tipo_prenda as tp inner join tipo_servicio as ts on tp.id_servicio=ts.id_tipo_servicio where tp.descripcion like concat("%",texto,"%") order by tp.descripcion ASC$$

CREATE DEFINER=`ticscode`@`%` PROCEDURE `spFiltrarProductos` (IN `p_descripcion` VARCHAR(180))   SELECT * FROM producto as p where p.descripcion like concat("%", p_descripcion, "%") order by p.descripcion asc$$

CREATE DEFINER=`ticscode`@`%` PROCEDURE `spGenerarOrden` (IN `p_id_cliente` INT, IN `p_num_orden` VARCHAR(20), IN `p_fecha_pedido` DATE, IN `p_fecha_entrega` DATE, IN `p_estado` VARCHAR(50), IN `p_saldo` FLOAT, IN `p_total` FLOAT, IN `p_id_usuario` INT, IN `p_observaciones` TEXT)   IF EXISTS(SELECT * FROM orden_trabajo AS o WHERE o.num_orden=p_num_orden) THEN
	SELECT 0;
ELSE
	INSERT INTO orden_trabajo (id_cliente, num_orden, fecha_pedido, fecha_entrega, estado, saldo,
                               total, id_usuario, observacion)
    VALUES (p_id_cliente, p_num_orden, p_fecha_pedido, p_fecha_entrega, UPPER(p_estado), p_saldo,
            p_total, p_id_usuario, p_observaciones);
    SELECT o.id_orden FROM orden_trabajo as o WHERE o.num_orden=p_num_orden;
END IF$$

CREATE DEFINER=`ticscode`@`%` PROCEDURE `spHistorialUsuarios` ()   BEGIN 
	SELECT caja.id_cierre, concat(u.nombres, '', u.apellidos) as responsable, date(caja.hora_apertura) as fecha, time(caja.hora_apertura) as hora_apertura, time(caja.hora_cierre) as hora_cierre, caja.total_ventas as total_vendido, caja.total_abono, caja.total_gastos, caja.observaciones FROM cierre_caja as caja 
    INNER JOIN usuario as u on caja.id_responsable=u.idUsuario;
END$$

CREATE DEFINER=`ticscode`@`%` PROCEDURE `spInventarioPrendas` ()   SELECT p.id_prenda, o.num_orden, c.nombres, tp.descripcion, ts.descripcion as servicio, o.fecha_entrega, o.estado, p.cantidad, p.precio_total, p.observacion  FROM prenda as p 
inner join tipo_prenda as tp on p.id_tipo_prenda=tp.id_prenda
inner join tipo_servicio as ts ON
p.id_servicio=ts.id_tipo_servicio
INNER join orden_trabajo as o on p.id_orden=o.id_orden
INNER JOIN cliente as c on o.id_cliente=c.idCliente
WHERE o.estado='PENDIENTE'$$

CREATE DEFINER=`ticscode`@`%` PROCEDURE `spObtenerClientePorId` (IN `p_id_cliente` INT)   SELECT * FROM cliente WHERE idCliente=p_id_cliente$$

CREATE DEFINER=`ticscode`@`%` PROCEDURE `spObtenerGastos` (IN `p_fecha` DATE)   SELECT rg.id_gasto, rg.fecha, rg.descripcion, rg.total, rg.id_cierre,
concat(u.nombres, ' ', u.apellidos) as responsable FROM registro_gastos as rg 
INNER JOIN usuario as u on rg.id_responsable=u.idUsuario
WHERE DATE(rg.fecha)=p_fecha$$

CREATE DEFINER=`ticscode`@`%` PROCEDURE `spObtenerIdPrenda` (IN `p_descripcion` VARCHAR(180))   SELECT tp.id_prenda FROM tipo_prenda AS tp WHERE tp.descripcion=p_descripcion$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `spObtenerIdProducto` (IN `p_descripcion` VARCHAR(180))   SELECT p.id_producto, p.cantidad, p.stock, p.observacion FROM producto AS p WHERE p.descripcion=p_descripcion$$

CREATE DEFINER=`ticscode`@`%` PROCEDURE `spObtenerIdServicio` (IN `p_descripcion` VARCHAR(50))   SELECT ts.id_tipo_servicio FROM tipo_servicio as ts WHERE ts.descripcion=p_descripcion$$

CREATE DEFINER=`ticscode`@`%` PROCEDURE `spObtenerMetodosPago` ()   SELECT m.metodo FROM metodo_pago as m$$

CREATE DEFINER=`ticscode`@`%` PROCEDURE `spObtenerOrden` (IN `p_num_orden` VARCHAR(20))   SELECT * FROM orden_trabajo WHERE num_orden=p_num_orden$$

CREATE DEFINER=`ticscode`@`%` PROCEDURE `spObtenerOrdenes` (IN `fecha` DATE)   SELECT o.id_orden, o.num_orden, o.fecha_pedido, o.fecha_entrega,
o.estado, o.saldo, o.total, c.nombres, c.cedula, c.telefono,c.email,
u.nombres as nom_usuario, u.apellidos FROM orden_trabajo AS o INNER JOIN cliente AS c 
ON o.id_cliente=c.idCliente INNER JOIN usuario AS u 
ON o.id_usuario=u.idUsuario
WHERE o.fecha_pedido=fecha$$

CREATE DEFINER=`ticscode`@`%` PROCEDURE `spObtenerOrdenesPorCliente` (IN `texto` VARCHAR(200))   BEGIN
	IF texto='' THEN
    	SELECT o.id_orden, o.num_orden, c.nombres, c.cedula,
        o.fecha_pedido, o.estado, o.fecha_entrega, o.saldo,
        o.total, concat(u.nombres, '', u.apellidos) as responsable
        FROM orden_trabajo as o 
        INNER JOIN cliente as c on o.id_cliente=c.idCliente
        INNER JOIN usuario as u on o.id_usuario=u.idUsuario;
    ELSE
    	SELECT o.id_orden, o.num_orden, c.nombres, c.cedula,
        o.fecha_pedido, o.estado, o.fecha_entrega, o.saldo,
        o.total, concat(u.nombres, '', u.apellidos) as responsable
        FROM orden_trabajo as o 
        INNER JOIN cliente as c on o.id_cliente=c.idCliente
        INNER JOIN usuario as u on o.id_usuario=u.idUsuario
        WHERE c.nombres like concat('%', texto, '%') or c.cedula=texto;
    END IF;
END$$

CREATE DEFINER=`ticscode`@`%` PROCEDURE `spObtenerPagos` (IN `fecha` DATE)   select pg.id_pago,  o.num_orden, o.fecha_pedido, c.nombres, o.fecha_entrega, o.estado, pg.saldo, pg.importe,
o.total, m.metodo, concat(u.nombres, ' ', u.apellidos) as responsable from pago_realizado as pg 
inner join orden_trabajo as  o on pg.id_orden=o.id_orden
inner join cliente as c on o.id_cliente=c.idCliente
inner join metodo_pago as m on pg.id_metodo=m.id_metodo
inner join cierre_caja as cc on pg.id_caja=cc.id_cierre
inner join usuario as u on cc.id_responsable=u.idUsuario
where pg.fecha_pago=fecha and date(cc.hora_apertura)=fecha ORDER BY o.num_orden, pg.saldo DESC$$

CREATE DEFINER=`ticscode`@`%` PROCEDURE `spObtenerPagosPorOrden` (IN `p_id_orden` INT)   SELECT pg.id_pago, pg.importe,pg.fecha_pago, m.metodo FROM pago_realizado AS pg INNER JOIN metodo_pago as m 
on pg.id_metodo = m.id_metodo WHERE pg.id_orden=p_id_orden$$

CREATE DEFINER=`ticscode`@`%` PROCEDURE `spObtenerPrecioPrenda` (IN `tipo_prenda` VARCHAR(180), IN `tipo_servicio` VARCHAR(60))   SELECT tp.precio FROM tipo_prenda as tp INNER JOIN tipo_servicio as ts
ON tp.id_servicio=ts.id_tipo_servicio 
WHERE tp.descripcion=tipo_prenda AND ts.descripcion=tipo_servicio$$

CREATE DEFINER=`ticscode`@`%` PROCEDURE `spObtenerPrendas` ()   SELECT tp.id_prenda, tp.descripcion, tp.precio, ts.descripcion as servicio from tipo_prenda as tp inner join tipo_servicio as ts on tp.id_servicio=ts.id_tipo_servicio order by tp.descripcion ASC$$

CREATE DEFINER=`ticscode`@`%` PROCEDURE `spObtenerPrendasPorPedido` (IN `p_id_orden` INT)   SELECT p.id_prenda, tp.descripcion, ts.descripcion as servicio,
p.cantidad, tp.precio, p.precio_total, p.observacion FROM prenda as p INNER JOIN tipo_prenda as tp 
ON p.id_tipo_prenda=tp.id_prenda 
INNER JOIN tipo_servicio as ts
ON p.id_servicio=ts.id_tipo_servicio
WHERE p.id_orden=p_id_orden$$

CREATE DEFINER=`ticscode`@`%` PROCEDURE `spObtenerPrendasPorServicio` (IN `p_servicio` VARCHAR(180))   SELECT tp.descripcion FROM tipo_prenda as tp 
INNER JOIN tipo_servicio as ts on tp.id_servicio=ts.id_tipo_servicio
WHERE ts.descripcion=p_servicio ORDER by tp.descripcion asc$$

CREATE DEFINER=`ticscode`@`%` PROCEDURE `spObtenerProductoPorDescripcion` (IN `p_descripcion` VARCHAR(180))   select * from producto as p where p.descripcion=p_descripcion$$

CREATE DEFINER=`ticscode`@`%` PROCEDURE `spObtenerProductos` ()   SELECT * FROM producto as p$$

CREATE DEFINER=`ticscode`@`%` PROCEDURE `spObtenerServicios` ()   SELECT * FROM tipo_servicio$$

CREATE DEFINER=`ticscode`@`%` PROCEDURE `spObtenerTipoPrenda` (IN `p_descripcion` VARCHAR(180))   select * from tipo_prenda as tp where tp.descripcion=upper(p_descripcion)$$

CREATE DEFINER=`ticscode`@`%` PROCEDURE `spRegistrarAperturaCaja` (IN `p_id_responsable` INT, IN `p_hora_apertura` DATETIME)   BEGIN
	INSERT INTO cierre_caja(id_responsable, hora_apertura,
	                       total_ventas, total_abono, total_gastos, observaciones)
	VALUES (p_id_responsable, p_hora_apertura, 0,
        0, 0, '');
    SELECT LAST_INSERT_ID();
END$$

CREATE DEFINER=`ticscode`@`%` PROCEDURE `spRegistrarCierreCaja` (IN `p_id_caja` INT, IN `p_hora` DATETIME, IN `p_total_ventas` FLOAT, IN `p_totaL_abonos` FLOAT, IN `p_total_gastos` FLOAT)   BEGIN 
	UPDATE cierre_caja as caja SET caja.hora_cierre=p_hora,
    caja.total_ventas=p_total_ventas, caja.total_abono=p_total_abonos,
    caja.total_gastos=p_total_gastos WHERE caja.id_cierre=p_id_caja;
END$$

CREATE DEFINER=`ticscode`@`%` PROCEDURE `spRegistrarCliente` (IN `p_nombres` VARCHAR(60), IN `p_direccion` VARCHAR(60), IN `p_telefono` VARCHAR(10), IN `p_email` VARCHAR(150), IN `ced` VARCHAR(10))   IF EXISTS(SELECT * FROM cliente as c WHERE c.cedula=ced) THEN
	SELECT 0;
ELSE
	INSERT INTO cliente(nombres, direccion, telefono, email, cedula) 
    VALUES (UPPER(p_nombres), UPPER(p_direccion), p_telefono, p_email, ced);
    
    SELECT c.idCliente FROM cliente as c WHERE c.cedula=ced;
END IF$$

CREATE DEFINER=`ticscode`@`%` PROCEDURE `spRegistrarGasto` (IN `p_fecha` DATETIME, IN `p_descripcion` VARCHAR(200), IN `p_total` FLOAT, IN `p_id_usuario` INT, IN `p_id_cierre` INT)   BEGIN
	INSERT INTO registro_gastos(fecha, descripcion, total, id_responsable,
                            id_cierre)
	VALUES(p_fecha, p_descripcion, p_total, p_id_usuario, p_id_cierre);
	SELECT LAST_INSERT_ID();
END$$

CREATE DEFINER=`ticscode`@`%` PROCEDURE `spRegistrarPago` (IN `p_importe` FLOAT, IN `p_id_orden` INT, IN `p_fecha_pago` DATE, IN `p_id_metodo` INT, IN `p_id_caja` INT, IN `p_saldo` FLOAT)   INSERT INTO pago_realizado(importe, id_orden, fecha_pago, id_metodo, id_caja, saldo)
VALUES(p_importe, p_id_orden, p_fecha_pago, p_id_metodo, p_id_caja, p_saldo)$$

CREATE DEFINER=`ticscode`@`%` PROCEDURE `spTotalizarGastos` (IN `p_fecha` DATE)   BEGIN
	SELECT round(sum(g.total), 2) FROM registro_gastos as g WHERE date(g.fecha)=p_fecha;
 END$$

CREATE DEFINER=`ticscode`@`%` PROCEDURE `spTotalizarImportes` (IN `p_fecha` DATE)   BEGIN
	SELECT round(SUM(pg.importe),2) FROM pago_realizado as pg WHERE date(pg.fecha_pago)=p_fecha;
END$$

CREATE DEFINER=`ticscode`@`%` PROCEDURE `spTotalizarVentas` (IN `p_fecha` DATE)   BEGIN
	SELECT round(SUM(o.total),2) FROM orden_trabajo AS o WHERE o.fecha_pedido=p_fecha;
END$$

CREATE DEFINER=`ticscode`@`%` PROCEDURE `spValidarUsuario` (IN `p_username` VARCHAR(60), IN `p_contrasenia` VARCHAR(60))   SELECT u.rol, u.nombres, u.apellidos, u.idUsuario FROM usuario as u WHERE u.username=p_username AND
u.contrasenia=MD5(p_contrasenia)$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cierre_caja`
--

CREATE TABLE `cierre_caja` (
  `id_cierre` int(11) NOT NULL,
  `id_responsable` int(11) NOT NULL,
  `hora_apertura` datetime NOT NULL,
  `hora_cierre` datetime DEFAULT NULL,
  `total_ventas` float NOT NULL,
  `total_abono` float NOT NULL,
  `total_gastos` float NOT NULL,
  `observaciones` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `cierre_caja`
--

INSERT INTO `cierre_caja` (`id_cierre`, `id_responsable`, `hora_apertura`, `hora_cierre`, `total_ventas`, `total_abono`, `total_gastos`, `observaciones`) VALUES
(1, 1, '2024-05-21 15:50:37', NULL, 0, 0, 0, ''),
(2, 1, '2024-05-21 15:53:58', NULL, 0, 0, 0, ''),
(3, 1, '2024-05-21 20:20:17', NULL, 0, 0, 0, ''),
(4, 1, '2024-05-22 07:56:30', NULL, 0, 0, 0, ''),
(5, 1, '2024-05-22 08:55:51', NULL, 0, 0, 0, ''),
(6, 1, '2024-05-22 11:25:53', NULL, 0, 0, 0, ''),
(7, 1, '2024-05-22 11:30:18', NULL, 0, 0, 0, ''),
(8, 1, '2024-05-22 11:55:34', NULL, 0, 0, 0, ''),
(9, 1, '2024-05-22 12:07:10', NULL, 0, 0, 0, ''),
(10, 1, '2024-05-22 12:09:03', NULL, 0, 0, 0, ''),
(11, 1, '2024-05-22 12:09:52', NULL, 0, 0, 0, ''),
(12, 1, '2024-05-22 12:28:37', NULL, 0, 0, 0, ''),
(13, 1, '2024-05-22 12:32:35', NULL, 0, 0, 0, ''),
(14, 1, '2024-05-22 12:34:36', NULL, 0, 0, 0, ''),
(15, 1, '2024-05-22 12:35:10', NULL, 0, 0, 0, ''),
(16, 1, '2024-05-22 12:37:33', NULL, 0, 0, 0, ''),
(17, 1, '2024-05-22 12:38:29', NULL, 0, 0, 0, ''),
(18, 1, '2024-05-22 12:40:43', NULL, 0, 0, 0, ''),
(19, 1, '2024-05-22 12:41:21', NULL, 0, 0, 0, ''),
(20, 1, '2024-05-22 12:42:55', NULL, 0, 0, 0, ''),
(21, 1, '2024-05-22 12:49:50', NULL, 0, 0, 0, ''),
(22, 1, '2024-05-22 12:50:16', NULL, 0, 0, 0, ''),
(23, 1, '2024-05-22 12:50:59', NULL, 0, 0, 0, ''),
(24, 1, '2024-05-22 13:08:17', NULL, 0, 0, 0, ''),
(25, 1, '2024-05-22 13:08:47', NULL, 0, 0, 0, ''),
(26, 1, '2024-05-22 13:09:36', NULL, 0, 0, 0, ''),
(27, 1, '2024-05-22 13:24:56', NULL, 0, 0, 0, ''),
(28, 1, '2024-05-22 13:26:31', NULL, 0, 0, 0, ''),
(29, 1, '2024-05-22 15:41:28', NULL, 0, 0, 0, ''),
(30, 1, '2024-05-22 15:44:55', NULL, 0, 0, 0, ''),
(31, 1, '2024-05-22 15:47:11', NULL, 0, 0, 0, ''),
(32, 1, '2024-05-22 15:49:16', NULL, 0, 0, 0, ''),
(33, 1, '2024-05-22 15:53:53', NULL, 0, 0, 0, ''),
(34, 1, '2024-05-22 16:03:42', NULL, 0, 0, 0, ''),
(35, 1, '2024-05-22 16:05:29', NULL, 0, 0, 0, ''),
(36, 1, '2024-05-22 16:06:24', NULL, 0, 0, 0, ''),
(37, 1, '2024-05-22 16:12:23', NULL, 0, 0, 0, ''),
(38, 1, '2024-05-22 16:14:05', NULL, 0, 0, 0, ''),
(39, 1, '2024-05-22 17:16:35', NULL, 0, 0, 0, ''),
(40, 1, '2024-05-22 17:18:02', NULL, 0, 0, 0, ''),
(41, 1, '2024-05-22 17:18:47', NULL, 0, 0, 0, ''),
(42, 1, '2024-05-22 17:21:32', NULL, 0, 0, 0, ''),
(43, 1, '2024-05-22 17:23:19', NULL, 0, 0, 0, ''),
(44, 1, '2024-05-22 17:28:48', NULL, 0, 0, 0, ''),
(45, 1, '2024-05-22 17:30:29', NULL, 0, 0, 0, ''),
(46, 1, '2024-05-22 17:31:01', NULL, 0, 0, 0, ''),
(47, 1, '2024-05-22 18:34:22', NULL, 0, 0, 0, ''),
(48, 1, '2024-05-22 18:35:14', NULL, 0, 0, 0, ''),
(49, 1, '2024-05-22 18:37:08', NULL, 0, 0, 0, ''),
(50, 1, '2024-05-22 18:45:11', NULL, 0, 0, 0, ''),
(51, 1, '2024-05-22 18:45:49', NULL, 0, 0, 0, ''),
(52, 1, '2024-05-22 18:50:45', NULL, 0, 0, 0, ''),
(53, 1, '2024-05-22 19:18:02', NULL, 0, 0, 0, ''),
(54, 1, '2024-05-22 19:19:37', NULL, 0, 0, 0, ''),
(55, 1, '2024-05-22 19:20:40', NULL, 0, 0, 0, ''),
(56, 1, '2024-05-22 20:48:18', NULL, 0, 0, 0, ''),
(57, 1, '2024-05-22 21:11:48', NULL, 0, 0, 0, ''),
(58, 1, '2024-05-22 21:29:56', NULL, 0, 0, 0, ''),
(59, 1, '2024-05-22 21:33:03', NULL, 0, 0, 0, ''),
(60, 1, '2024-05-22 21:35:33', NULL, 0, 0, 0, ''),
(61, 1, '2024-05-22 21:36:53', NULL, 0, 0, 0, ''),
(62, 1, '2024-05-22 21:38:10', NULL, 0, 0, 0, ''),
(63, 1, '2024-05-23 00:32:04', NULL, 0, 0, 0, ''),
(64, 1, '2024-05-23 01:03:28', NULL, 0, 0, 0, ''),
(65, 1, '2024-05-23 01:08:52', NULL, 0, 0, 0, ''),
(66, 1, '2024-05-23 01:09:57', NULL, 0, 0, 0, ''),
(67, 1, '2024-05-23 01:11:04', NULL, 0, 0, 0, ''),
(68, 1, '2024-05-23 01:12:36', NULL, 0, 0, 0, ''),
(69, 1, '2024-05-23 01:15:47', NULL, 0, 0, 0, ''),
(70, 1, '2024-05-23 01:17:50', NULL, 0, 0, 0, ''),
(71, 1, '2024-05-23 01:19:34', NULL, 0, 0, 0, ''),
(72, 1, '2024-05-23 01:20:24', NULL, 0, 0, 0, ''),
(73, 1, '2024-05-23 01:24:57', NULL, 0, 0, 0, ''),
(74, 1, '2024-05-23 01:26:01', NULL, 0, 0, 0, ''),
(75, 1, '2024-05-23 01:30:22', NULL, 0, 0, 0, ''),
(76, 1, '2024-05-23 01:30:59', NULL, 0, 0, 0, ''),
(77, 1, '2024-05-23 01:43:55', NULL, 0, 0, 0, ''),
(78, 1, '2024-05-23 01:44:31', NULL, 0, 0, 0, ''),
(79, 1, '2024-05-23 10:27:56', NULL, 0, 0, 0, ''),
(80, 1, '2024-05-23 11:44:55', NULL, 0, 0, 0, ''),
(81, 1, '2024-05-23 12:55:29', NULL, 0, 0, 0, ''),
(82, 1, '2024-05-23 14:44:11', NULL, 0, 0, 0, ''),
(83, 1, '2024-05-23 17:05:58', NULL, 0, 0, 0, ''),
(84, 1, '2024-05-23 17:07:03', NULL, 0, 0, 0, ''),
(85, 1, '2024-05-23 17:11:14', NULL, 0, 0, 0, ''),
(86, 1, '2024-05-23 17:14:10', NULL, 0, 0, 0, ''),
(87, 1, '2024-05-23 17:16:20', NULL, 0, 0, 0, ''),
(88, 1, '2024-05-23 17:31:28', NULL, 0, 0, 0, ''),
(89, 1, '2024-05-23 17:33:34', NULL, 0, 0, 0, ''),
(90, 1, '2024-05-23 17:46:32', NULL, 0, 0, 0, ''),
(91, 1, '2024-05-23 17:47:53', NULL, 0, 0, 0, ''),
(92, 1, '2024-05-23 18:06:28', NULL, 0, 0, 0, ''),
(93, 1, '2024-05-23 18:08:57', NULL, 0, 0, 0, ''),
(94, 1, '2024-05-23 18:11:47', NULL, 0, 0, 0, ''),
(95, 1, '2024-05-23 18:56:10', NULL, 0, 0, 0, ''),
(96, 1, '2024-05-23 18:58:22', NULL, 0, 0, 0, ''),
(97, 1, '2024-05-23 19:00:33', NULL, 0, 0, 0, ''),
(98, 1, '2024-05-24 20:02:19', NULL, 0, 0, 0, ''),
(99, 1, '2024-05-24 22:11:26', NULL, 0, 0, 0, ''),
(100, 1, '2024-05-25 08:47:20', NULL, 0, 0, 0, ''),
(101, 1, '2024-05-25 12:39:04', NULL, 0, 0, 0, ''),
(102, 1, '2024-05-25 12:41:23', NULL, 0, 0, 0, ''),
(103, 1, '2024-05-25 12:45:31', NULL, 0, 0, 0, ''),
(104, 1, '2024-05-26 13:16:02', NULL, 0, 0, 0, ''),
(105, 1, '2024-05-27 15:05:59', NULL, 0, 0, 0, ''),
(106, 1, '2024-05-27 16:53:46', NULL, 0, 0, 0, ''),
(107, 1, '2024-05-27 18:27:19', NULL, 0, 0, 0, ''),
(108, 1, '2024-05-27 18:46:43', NULL, 0, 0, 0, ''),
(109, 1, '2024-05-27 18:50:06', NULL, 0, 0, 0, ''),
(110, 1, '2024-05-27 18:53:02', NULL, 0, 0, 0, ''),
(111, 1, '2024-05-27 19:02:09', NULL, 0, 0, 0, ''),
(112, 1, '2024-05-27 19:33:48', NULL, 0, 0, 0, ''),
(113, 1, '2024-05-27 19:35:24', NULL, 0, 0, 0, ''),
(114, 1, '2024-05-27 19:36:52', NULL, 0, 0, 0, ''),
(115, 1, '2024-05-27 19:41:52', NULL, 0, 0, 0, ''),
(116, 1, '2024-05-27 20:40:37', NULL, 0, 0, 0, ''),
(117, 1, '2024-05-27 20:44:54', NULL, 0, 0, 0, ''),
(118, 1, '2024-05-27 20:58:13', NULL, 0, 0, 0, ''),
(119, 1, '2024-05-28 02:14:46', '2024-05-28 02:16:09', 0, 0, 0, ''),
(120, 1, '2024-05-28 02:33:34', NULL, 0, 0, 0, ''),
(121, 1, '2024-05-28 02:35:16', NULL, 0, 0, 0, ''),
(122, 1, '2024-05-28 02:35:59', '2024-05-28 02:36:57', 20, 10, 0, ''),
(123, 1, '2024-05-28 02:43:25', NULL, 0, 0, 0, ''),
(124, 1, '2024-05-28 02:46:16', NULL, 0, 0, 0, ''),
(125, 1, '2024-05-29 16:49:50', NULL, 0, 0, 0, ''),
(126, 1, '2024-05-29 17:02:07', NULL, 0, 0, 0, ''),
(127, 1, '2024-05-29 17:02:52', NULL, 0, 0, 0, ''),
(128, 1, '2024-05-29 17:05:54', NULL, 0, 0, 0, ''),
(129, 1, '2024-05-29 17:06:37', NULL, 0, 0, 0, ''),
(130, 1, '2024-05-29 17:07:38', NULL, 0, 0, 0, ''),
(131, 1, '2024-05-29 17:08:53', NULL, 0, 0, 0, '');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cliente`
--

CREATE TABLE `cliente` (
  `idCliente` int(11) NOT NULL,
  `nombres` varchar(50) NOT NULL,
  `direccion` varchar(60) NOT NULL,
  `telefono` varchar(10) NOT NULL,
  `email` varchar(128) DEFAULT NULL,
  `cedula` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `cliente`
--

INSERT INTO `cliente` (`idCliente`, `nombres`, `direccion`, `telefono`, `email`, `cedula`) VALUES
(4, 'JEFFERSON  ALFARO', 'COMITE DEL PUEBLO', '0979112697', 'alfaro.jefferson96@gmail.com', '1724155492'),
(5, 'CRISTIAN GARCIA', 'COMITE DEL PUEBLO', '0979112697', 'cg@gmail.com', '1711253658'),
(7, 'AYALA BUENAÑO ISABEL', 'SAN ISIDRO', '0996039085', 'anaiayalaB@hotmail.com', '1709598591'),
(17, 'NARCISA ESPINOZA', 'COMITE DEL PUEBLO', '12345688', 'alfaro.jefferson', '1714205075'),
(20, 'CONSUMIDOR FINAL', 'República dominicana N79-59 y Francisco Ruiz', '0961026492', 'lavanderiasAzules@gmail.com', '9999999999'),
(24, 'GARCIA MARGARITA', 'CARCELÉN', '0999802814', 'alfredh2016@hotmail.com', '1720108982'),
(25, 'GUARICELA PALACIO JORGE PATRICIO', 'CARCELÉN', '0987978747', 'romulo_ortiz@icloud.com', '0101947158');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `metodo_pago`
--

CREATE TABLE `metodo_pago` (
  `id_metodo` int(11) NOT NULL,
  `metodo` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `metodo_pago`
--

INSERT INTO `metodo_pago` (`id_metodo`, `metodo`) VALUES
(1, 'EFECTIVO'),
(2, 'TRANSFERENCIA');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `orden_trabajo`
--

CREATE TABLE `orden_trabajo` (
  `id_orden` int(11) NOT NULL,
  `id_cliente` int(11) NOT NULL,
  `num_orden` varchar(15) NOT NULL,
  `fecha_pedido` date NOT NULL,
  `fecha_entrega` date NOT NULL,
  `estado` varchar(64) NOT NULL,
  `saldo` float NOT NULL,
  `total` float NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `observacion` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `orden_trabajo`
--

INSERT INTO `orden_trabajo` (`id_orden`, `id_cliente`, `num_orden`, `fecha_pedido`, `fecha_entrega`, `estado`, `saldo`, `total`, `id_usuario`, `observacion`) VALUES
(1217014, 4, '1217014', '2024-05-23', '2024-05-24', 'PENDIENTE', 2.5, 5, 1, ''),
(1217015, 4, '1217015', '2024-05-25', '2024-05-25', 'ENTREGADO', 0, 11, 1, ''),
(1217016, 4, '1217016', '2024-05-25', '2024-05-26', 'ENTREGADO', 0, 6, 1, ''),
(1217017, 4, '1217017', '2024-05-26', '2024-05-27', 'PENDIENTE', 4.6, 7.6, 1, ''),
(1217018, 4, '1217018', '2024-05-27', '2024-05-27', 'ENTREGADO', 0, 6, 1, ''),
(1217019, 25, '1217019', '2024-05-28', '2024-05-29', 'PENDIENTE', 10, 20, 1, '');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pago_realizado`
--

CREATE TABLE `pago_realizado` (
  `id_pago` int(11) NOT NULL,
  `importe` float NOT NULL,
  `id_orden` int(11) NOT NULL,
  `fecha_pago` date NOT NULL,
  `id_metodo` int(11) NOT NULL,
  `id_caja` int(11) NOT NULL,
  `saldo` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `pago_realizado`
--

INSERT INTO `pago_realizado` (`id_pago`, `importe`, `id_orden`, `fecha_pago`, `id_metodo`, `id_caja`, `saldo`) VALUES
(6, 2.5, 1217014, '2024-05-23', 1, 97, 2.5),
(7, 10, 1217015, '2024-05-25', 1, 102, 1),
(8, 1, 1217015, '2024-05-25', 2, 102, 0),
(9, 3, 1217016, '2024-05-25', 1, 103, 3),
(10, 3, 1217016, '2024-05-26', 2, 104, 0),
(11, 3, 1217018, '2024-05-27', 1, 105, 3),
(12, 3, 1217018, '2024-05-27', 2, 115, 0),
(13, 10, 1217019, '2024-05-28', 1, 122, 10);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `prenda`
--

CREATE TABLE `prenda` (
  `id_prenda` int(11) NOT NULL,
  `id_tipo_prenda` int(11) NOT NULL,
  `id_servicio` int(11) NOT NULL,
  `cantidad` int(11) NOT NULL,
  `precio_total` float NOT NULL,
  `observacion` varchar(200) DEFAULT NULL,
  `id_orden` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `prenda`
--

INSERT INTO `prenda` (`id_prenda`, `id_tipo_prenda`, `id_servicio`, `cantidad`, `precio_total`, `observacion`, `id_orden`) VALUES
(12, 8, 1, 2, 5, '', 1217014),
(13, 93, 1, 2, 11, '', 1217015),
(14, 78, 4, 1, 6, 'Camisa polo', 1217016),
(15, 80, 2, 1, 3, '', 1217017),
(16, 81, 2, 1, 3, '', 1217017),
(17, 80, 2, 1, 3, '', 1217018),
(18, 81, 2, 1, 3, '', 1217018),
(19, 2, 1, 2, 20, '', 1217019);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `producto`
--

CREATE TABLE `producto` (
  `id_producto` int(11) NOT NULL,
  `descripcion` varchar(100) NOT NULL,
  `cantidad` int(11) NOT NULL,
  `stock` int(11) NOT NULL,
  `precio` float NOT NULL,
  `observacion` varchar(180) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `producto`
--

INSERT INTO `producto` (`id_producto`, `descripcion`, `cantidad`, `stock`, `precio`, `observacion`) VALUES
(1, 'CLORO', 6, 1, 0.2, ''),
(2, 'CLORO COLOR', 14, 1, 0.85, ''),
(3, 'CLORO DECOLOR', 1, 1, 0.85, ''),
(4, 'CLORO JUMBO', 1, 1, 0.35, ''),
(5, 'CLOROX ROPA COLOR 250 ML', 1, 1, 1.25, ''),
(6, 'DESENGRASANTE', 1, 1, 0.4, ''),
(7, 'DETERGENTE 100 GR', 1, 1, 0.5, ''),
(8, 'DETERGENTE 135 GR', 0, 1, 0.6, ''),
(9, 'DEJA 150 GR', 1, 1, 0.6, ''),
(10, 'DETERGENTE 360 GR ', 1, 1, 1, ''),
(11, 'DETERGENTE 540 GR', 1, 1, 1.5, ''),
(12, 'DETERGENTE 60 GR', 1, 1, 0.25, ''),
(13, 'JABÓN LIQUIDO 300 ML', 1, 1, 1, ''),
(14, 'JABÓN LÍQUIDO 210 ML', 1, 1, 0.8, ''),
(15, 'JABÓN LÍQUIDO 350 ML', 1, 1, 1.2, ''),
(16, 'JABÓN LÍQUIDO 70 ML', 1, 1, 0.4, ''),
(17, 'SUAVIZANTE 70 ML', 0, 1, 0.4, ''),
(18, 'SUAVITEL 50 ML', 1, 1, 0.4, ''),
(19, 'SUAVITEL 110-115 ML', 1, 0, 0.7, ''),
(20, 'SUAVITEL 210 ML ', 0, 1, 1, ''),
(21, 'SUAVITEL 425-430 ML', 1, 1, 1.5, '');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `registro_gastos`
--

CREATE TABLE `registro_gastos` (
  `id_gasto` int(11) NOT NULL,
  `fecha` datetime NOT NULL,
  `descripcion` varchar(200) NOT NULL,
  `total` float NOT NULL,
  `id_responsable` int(11) NOT NULL,
  `id_cierre` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `registro_gastos`
--

INSERT INTO `registro_gastos` (`id_gasto`, `fecha`, `descripcion`, `total`, `id_responsable`, `id_cierre`) VALUES
(1, '2024-05-25 12:43:34', 'COMPRA GAS', 3.75, 1, 102),
(2, '2024-05-26 13:32:45', 'GAS', 2, 1, 104);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tipo_prenda`
--

CREATE TABLE `tipo_prenda` (
  `id_prenda` int(11) NOT NULL,
  `descripcion` varchar(180) NOT NULL,
  `precio` float NOT NULL,
  `id_servicio` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `tipo_prenda`
--

INSERT INTO `tipo_prenda` (`id_prenda`, `descripcion`, `precio`, `id_servicio`) VALUES
(1, 'ABRIGO LIVIANO O GABARDINA', 8, 1),
(2, 'ABRIGO PESADO O PIEL', 10, 1),
(3, 'ALFOMBRA DELGADA (POR M2)', 5, 1),
(4, 'ALFOMBRA GRUESA (POR M2)', 5.5, 1),
(5, 'ALMOHADAS', 4, 1),
(6, 'BLUSA/MANDIL EN SECO', 2.5, 1),
(7, 'BUFANDAS', 2, 1),
(8, 'CAMISA EN SECO', 2.5, 1),
(9, 'CAMISA EN AGUA', 2, 1),
(10, 'CAMISA SOLO PLANCHADO', 1.25, 1),
(11, 'CAPA NIÑO + BIRRETE', 5, 1),
(12, 'CAPA MEDIANA + BIRRETE', 6, 1),
(13, 'CAPA GRANDE + BIRRETE ', 7, 1),
(14, 'COBIJA 1 PLAZA', 5, 5),
(15, 'COBIJA 1 1/2 PLAZA', 5.5, 5),
(16, 'COBIJA 2 PLAZAS GRANDE', 6, 5),
(17, 'CORBATA SIMPLE', 2, 1),
(18, 'CORTINA LIVIANA M2', 3, 1),
(19, 'CORTINA PESADA M2', 3.5, 1),
(20, 'COJINES PEQUEÑOS', 3, 1),
(21, 'COJINES MEDIANOS', 4, 1),
(22, 'COJINES GRANDES', 6, 1),
(23, 'CUBREMANTELES', 4, 1),
(24, 'CHALES CON ADORNOS DELICADOS', 4, 1),
(25, 'CHALES Y PONCHOS EN GENERAL', 5, 1),
(26, 'CHAQUETAS', 3.5, 1),
(27, 'CHOMPA LIVIANA DE CUERO O GAMUSA', 12, 1),
(28, 'CHOMPA PESADA DE CUERO O GAMUSA', 15, 1),
(29, 'CHOMPAS LIVIANAS', 4, 1),
(30, 'CHOMPAS PESADAS', 4.5, 1),
(31, 'CHOMPA CAMUFLASH', 4.5, 1),
(32, 'EDREDÓN 1 PLAZA', 6, 5),
(33, 'EDREDÓN 1 1/2 PLAZAS', 6, 5),
(34, 'EDREDÓN 2 PLAZAS', 7, 5),
(35, 'ENTERIZOS', 5, 1),
(36, 'FALDA PLIZADA', 4.5, 1),
(37, 'FALDONES GRANDES', 3.5, 1),
(38, 'FALDONES MEDIANOS', 3, 1),
(39, 'FALDONES_PEQUEÑOS', 2.5, 1),
(40, 'FORRO DE SILLA', 2, 1),
(41, 'GORRAS, JOCKEY O MUCETA', 2.5, 1),
(42, 'JUEGO DE SABANAS + 2 FUNDAS', 3.5, 1),
(43, 'MANTEL STANDARD BORDADO', 6, 1),
(44, 'MANTEL STANDARD SENCILLO', 5, 1),
(45, 'MOCHILA', 4, 1),
(46, 'MALETA MEDIANA', 6, 1),
(47, 'MALETA GRANDE', 10, 1),
(48, 'OVEROL', 5, 1),
(49, 'PAÑOLETAS DE MUJER', 2, 1),
(50, 'PAÑOS DE MESA M2', 2, 1),
(51, 'PANTALÓN/FALDA', 3.5, 1),
(52, 'PANTALÓN/FALDA SOLO PLANCHADO', 1.75, 1),
(53, 'PELUCHE EXTRAGRANDE', 20, 1),
(54, 'PELUCHE GRANDE', 15, 1),
(55, 'PELUCHE MEDIANO', 7, 1),
(56, 'PELUCHE PEQUEÑO', 4.5, 1),
(57, 'PULOVER, LICRAS', 3.5, 1),
(58, 'ROMPEVIENTOS O SIMILAR EN SECO', 4.5, 1),
(59, 'SACO/SWETER', 3.5, 1),
(60, 'TERNO 2 PIEZAS', 2, 1),
(63, 'TERNO SOLO PLANCHADO', 3.5, 1),
(64, 'TERNO 3 PIEZAS', 8.5, 1),
(65, 'TERNO MUJER CON VESTIDO', 7.5, 1),
(66, 'TERNO NIÑO', 6, 1),
(67, 'TERNO CAMUFLASH', 6, 1),
(68, 'TOGA + BIRRETE', 7, 1),
(69, 'VESTIDO CON ADORNOS COMPLICADOS', 8, 1),
(70, 'VESTIDO CON ADORNOS SENCILLOS', 6, 1),
(71, 'VESTIDO DE NOVIA SENCILLO', 16, 1),
(72, 'VESTIDO DE NOVIA CON COLA Y VELO', 22, 1),
(73, 'VESTIDO DE 15 AÑOS', 12, 1),
(74, 'VESTIDO SIMPLE O DE NIÑA', 4.5, 1),
(75, 'VESTIDO DE FIESTA', 7, 1),
(76, 'ZAPATOS', 4, 1),
(77, 'TINTURADO NORMAL', 4.5, 4),
(78, 'TINTURADO GRANDE', 6, 4),
(79, 'TINTURADO AL COSTO', 2, 4),
(80, 'AUTOSERVICIO LAVADO', 3, 2),
(81, 'AUTOSERVICIO SECADO', 3, 2),
(82, 'AUTOSERVICIO CENTRIFUGADO', 1.5, 2),
(93, 'COBIJA 1 1/2 PLAZA S', 5.5, 1),
(94, 'COBIJA 1 PLAZA S', 5, 1),
(95, 'COBIJA 2 PLAZAS GRANDES S', 6, 1),
(96, 'EDREDÓN 1 1/2 PLAZAS  S', 6, 1),
(97, 'EDREDÓN 1 PLAZA S', 6, 1),
(98, 'EDREDÓN 2 PLAZAS S', 7, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tipo_servicio`
--

CREATE TABLE `tipo_servicio` (
  `id_tipo_servicio` int(11) NOT NULL,
  `descripcion` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `tipo_servicio`
--

INSERT INTO `tipo_servicio` (`id_tipo_servicio`, `descripcion`) VALUES
(1, 'SECO'),
(2, 'LOCAL'),
(3, 'PRODUCTO'),
(4, 'TINTURADO'),
(5, 'PLANTA AZUL');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario`
--

CREATE TABLE `usuario` (
  `idUsuario` int(11) NOT NULL,
  `nombres` varchar(50) NOT NULL,
  `apellidos` varchar(50) NOT NULL,
  `username` varchar(50) NOT NULL,
  `contrasenia` varchar(128) NOT NULL,
  `rol` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuario`
--

INSERT INTO `usuario` (`idUsuario`, `nombres`, `apellidos`, `username`, `contrasenia`, `rol`) VALUES
(1, 'TICSCODE', 'ADMIN', 'ticscode', '31d4ab5d1dc00dcb75cfc32a26c82cd9', 'admin');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `cierre_caja`
--
ALTER TABLE `cierre_caja`
  ADD PRIMARY KEY (`id_cierre`),
  ADD KEY `fkResponsableCaja` (`id_responsable`);

--
-- Indices de la tabla `cliente`
--
ALTER TABLE `cliente`
  ADD PRIMARY KEY (`idCliente`);

--
-- Indices de la tabla `metodo_pago`
--
ALTER TABLE `metodo_pago`
  ADD PRIMARY KEY (`id_metodo`);

--
-- Indices de la tabla `orden_trabajo`
--
ALTER TABLE `orden_trabajo`
  ADD PRIMARY KEY (`id_orden`),
  ADD KEY `fkCliente` (`id_cliente`),
  ADD KEY `fkUsuario` (`id_usuario`);

--
-- Indices de la tabla `pago_realizado`
--
ALTER TABLE `pago_realizado`
  ADD PRIMARY KEY (`id_pago`),
  ADD KEY `fkPagoOrden` (`id_orden`),
  ADD KEY `fkMetodoPago` (`id_metodo`),
  ADD KEY `fkCajaTurno` (`id_caja`);

--
-- Indices de la tabla `prenda`
--
ALTER TABLE `prenda`
  ADD PRIMARY KEY (`id_prenda`),
  ADD KEY `fkTipoPrenda` (`id_tipo_prenda`),
  ADD KEY `fkTipoServicio` (`id_servicio`),
  ADD KEY `fkOrden` (`id_orden`);

--
-- Indices de la tabla `producto`
--
ALTER TABLE `producto`
  ADD PRIMARY KEY (`id_producto`);

--
-- Indices de la tabla `registro_gastos`
--
ALTER TABLE `registro_gastos`
  ADD PRIMARY KEY (`id_gasto`),
  ADD KEY `fkResponsable` (`id_responsable`),
  ADD KEY `fkCaja` (`id_cierre`);

--
-- Indices de la tabla `tipo_prenda`
--
ALTER TABLE `tipo_prenda`
  ADD PRIMARY KEY (`id_prenda`),
  ADD KEY `fkServicio` (`id_servicio`);

--
-- Indices de la tabla `tipo_servicio`
--
ALTER TABLE `tipo_servicio`
  ADD PRIMARY KEY (`id_tipo_servicio`);

--
-- Indices de la tabla `usuario`
--
ALTER TABLE `usuario`
  ADD PRIMARY KEY (`idUsuario`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `cierre_caja`
--
ALTER TABLE `cierre_caja`
  MODIFY `id_cierre` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=132;

--
-- AUTO_INCREMENT de la tabla `cliente`
--
ALTER TABLE `cliente`
  MODIFY `idCliente` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- AUTO_INCREMENT de la tabla `metodo_pago`
--
ALTER TABLE `metodo_pago`
  MODIFY `id_metodo` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `orden_trabajo`
--
ALTER TABLE `orden_trabajo`
  MODIFY `id_orden` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1217020;

--
-- AUTO_INCREMENT de la tabla `pago_realizado`
--
ALTER TABLE `pago_realizado`
  MODIFY `id_pago` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT de la tabla `prenda`
--
ALTER TABLE `prenda`
  MODIFY `id_prenda` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT de la tabla `producto`
--
ALTER TABLE `producto`
  MODIFY `id_producto` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT de la tabla `registro_gastos`
--
ALTER TABLE `registro_gastos`
  MODIFY `id_gasto` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `tipo_prenda`
--
ALTER TABLE `tipo_prenda`
  MODIFY `id_prenda` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=99;

--
-- AUTO_INCREMENT de la tabla `tipo_servicio`
--
ALTER TABLE `tipo_servicio`
  MODIFY `id_tipo_servicio` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `usuario`
--
ALTER TABLE `usuario`
  MODIFY `idUsuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `cierre_caja`
--
ALTER TABLE `cierre_caja`
  ADD CONSTRAINT `fkResponsableCaja` FOREIGN KEY (`id_responsable`) REFERENCES `usuario` (`idUsuario`);

--
-- Filtros para la tabla `orden_trabajo`
--
ALTER TABLE `orden_trabajo`
  ADD CONSTRAINT `fkCliente` FOREIGN KEY (`id_cliente`) REFERENCES `cliente` (`idCliente`),
  ADD CONSTRAINT `fkUsuario` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`idUsuario`);

--
-- Filtros para la tabla `pago_realizado`
--
ALTER TABLE `pago_realizado`
  ADD CONSTRAINT `fkCajaTurno` FOREIGN KEY (`id_caja`) REFERENCES `cierre_caja` (`id_cierre`),
  ADD CONSTRAINT `fkMetodoPago` FOREIGN KEY (`id_metodo`) REFERENCES `metodo_pago` (`id_metodo`),
  ADD CONSTRAINT `fkPagoOrden` FOREIGN KEY (`id_orden`) REFERENCES `orden_trabajo` (`id_orden`);

--
-- Filtros para la tabla `prenda`
--
ALTER TABLE `prenda`
  ADD CONSTRAINT `fkOrden` FOREIGN KEY (`id_orden`) REFERENCES `orden_trabajo` (`id_orden`),
  ADD CONSTRAINT `fkTipoPrenda` FOREIGN KEY (`id_tipo_prenda`) REFERENCES `tipo_prenda` (`id_prenda`),
  ADD CONSTRAINT `fkTipoServicio` FOREIGN KEY (`id_servicio`) REFERENCES `tipo_servicio` (`id_tipo_servicio`);

--
-- Filtros para la tabla `registro_gastos`
--
ALTER TABLE `registro_gastos`
  ADD CONSTRAINT `fkCaja` FOREIGN KEY (`id_cierre`) REFERENCES `cierre_caja` (`id_cierre`),
  ADD CONSTRAINT `fkResponsable` FOREIGN KEY (`id_responsable`) REFERENCES `usuario` (`idUsuario`);

--
-- Filtros para la tabla `tipo_prenda`
--
ALTER TABLE `tipo_prenda`
  ADD CONSTRAINT `fkServicio` FOREIGN KEY (`id_servicio`) REFERENCES `tipo_servicio` (`id_tipo_servicio`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
